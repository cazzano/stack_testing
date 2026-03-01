"""
TRUE Webhook — Production Grade
================================
Fixes applied:
  4. Notifications loaded from Postgres on startup (survives restarts)
  5. Fully async listener using asyncpg — no threads, no blocking
  6. Structured logging with log levels and file rotation

Flow:
  Postgres INSERT
    → pg trigger fires NOTIFY instantly
    → asyncpg listener wakes (fully async, zero thread overhead)
    → pushes directly to SSE clients + logs in memory
    → notify.py CLI receives it instantly via open SSE stream
"""

import asyncio
import json
import logging
import logging.handlers
import os
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime

import asyncpg
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Text, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
PORT              = int(os.getenv("PORT", 8000))
MAX_NOTIFICATIONS = int(os.getenv("MAX_NOTIFICATIONS", 500))
DB_HOST           = os.getenv("DB_HOST", "localhost")
DB_PORT           = int(os.getenv("DB_PORT", 5432))
DB_NAME           = os.getenv("DB_NAME", "notify")
DB_USER           = os.getenv("DB_USER", "postgres")
DB_PASSWORD       = os.getenv("DB_PASSWORD", "postgres")
LOG_FILE          = "webhook.log"

SQLALCHEMY_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNCPG_DSN    = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ──────────────────────────────────────────────
# FIX 6 — LOGGING FRAMEWORK
# ──────────────────────────────────────────────
def setup_logging():
    logger = logging.getLogger("webhook")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console — INFO and above
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)

    # Rotating file — DEBUG and above, 5MB per file, 3 backups
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


log = setup_logging()

# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────
engine       = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Notification(Base):
    __tablename__ = "notifications"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    notification = Column(Text, nullable=False)


def setup_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE OR REPLACE FUNCTION notify_new_notification()
            RETURNS TRIGGER AS $$
            BEGIN
                PERFORM pg_notify(
                    'new_notification',
                    json_build_object('id', NEW.id, 'notification', NEW.notification)::text
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """))
        conn.execute(text("DROP TRIGGER IF EXISTS trg_notify_new_notification ON notifications;"))
        conn.execute(text("""
            CREATE TRIGGER trg_notify_new_notification
            AFTER INSERT ON notifications
            FOR EACH ROW EXECUTE FUNCTION notify_new_notification();
        """))
        conn.commit()
    log.info("Table + NOTIFY trigger ready.")


# ──────────────────────────────────────────────
# FIX 4 — LOAD EXISTING NOTIFICATIONS ON STARTUP
# ──────────────────────────────────────────────
def load_existing_notifications() -> deque:
    """Read the last MAX_NOTIFICATIONS rows from Postgres on startup."""
    db   = SessionLocal()
    rows = (
        db.query(Notification)
        .order_by(Notification.id.desc())
        .limit(MAX_NOTIFICATIONS)
        .all()
    )
    db.close()
    existing = deque(maxlen=MAX_NOTIFICATIONS)
    for row in reversed(rows):
        existing.append({
            "id":           row.id,
            "notification": row.notification,
            "received_at":  None,
        })
    log.info(f"Loaded {len(existing)} existing notifications from Postgres.")
    return existing


# ──────────────────────────────────────────────
# SSE MANAGER
# ──────────────────────────────────────────────
class SSEManager:
    def __init__(self):
        self._queues: list[asyncio.Queue] = []

    def add_client(self) -> asyncio.Queue:
        q = asyncio.Queue()
        self._queues.append(q)
        log.info(f"SSE client connected ({len(self._queues)} total)")
        return q

    def remove_client(self, q: asyncio.Queue):
        if q in self._queues:
            self._queues.remove(q)
        log.info(f"SSE client disconnected ({len(self._queues)} remaining)")

    async def broadcast(self, data: dict):
        dead = []
        for q in self._queues:
            try:
                await q.put(data)
            except Exception:
                dead.append(q)
        for q in dead:
            self._queues.remove(q)


sse_manager = SSEManager()
received_notifications: deque[dict] = deque(maxlen=MAX_NOTIFICATIONS)


# ──────────────────────────────────────────────
# FIX 5 — ASYNC POSTGRES LISTENER (asyncpg)
# No threads. No blocking. Pure async.
# ──────────────────────────────────────────────
async def pg_listener():
    """
    Uses asyncpg to LISTEN on 'new_notification'.
    Fully async — no background thread, no select(), no blocking.
    Pushes directly to SSE clients and in-memory log.
    Auto-reconnects with exponential backoff if Postgres restarts.
    """
    backoff = 1
    conn    = None

    while True:
        try:
            conn    = await asyncpg.connect(ASYNCPG_DSN)
            backoff = 1
            log.info("asyncpg connected — LISTENing on 'new_notification'...")

            async def on_notify(connection, pid, channel, payload):
                data  = json.loads(payload)
                entry = {
                    "id":           data["id"],
                    "notification": data["notification"],
                    "received_at":  datetime.utcnow().isoformat(),
                }
                log.info(f"NOTIFY received → id={entry['id']} | '{entry['notification']}'")
                received_notifications.append(entry)
                await sse_manager.broadcast(entry)

            await conn.add_listener("new_notification", on_notify)

            # Yield control — asyncpg fires on_notify automatically on NOTIFY
            while True:
                await asyncio.sleep(1)

        except (asyncpg.PostgresConnectionError, OSError) as e:
            log.warning(f"Postgres connection lost: {e}. Reconnecting in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)

        except asyncio.CancelledError:
            log.info("pg_listener shutting down.")
            break

        except Exception as e:
            log.error(f"Unexpected listener error: {e}. Retrying in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)

        finally:
            if conn and not conn.is_closed():
                try:
                    await conn.remove_listener("new_notification", on_notify)
                    await conn.close()
                except Exception:
                    pass


# ──────────────────────────────────────────────
# SCHEMAS
# ──────────────────────────────────────────────
class NotificationCreate(BaseModel):
    notification: str
    model_config = {"json_schema_extra": {"example": {"notification": "CPU above 90% on server-01"}}}


# ──────────────────────────────────────────────
# LIFESPAN
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global received_notifications
    setup_db()
    received_notifications = load_existing_notifications()  # FIX 4
    listener_task = asyncio.create_task(pg_listener())      # FIX 5
    log.info(f"App ready — Docs: http://127.0.0.1:{PORT}/docs")
    log.info(f"SSE stream: http://127.0.0.1:{PORT}/webhook/stream")
    yield
    listener_task.cancel()
    await asyncio.gather(listener_task, return_exceptions=True)
    log.info("Shutdown complete.")


# ──────────────────────────────────────────────
# APP
# ──────────────────────────────────────────────
app = FastAPI(
    title="True Notification Webhook",
    description=f"""
## 🔔 True Webhook — Production Grade

**Zero polling. Persistent. Fully async.**

### Fixes applied
| # | Fix | How |
|---|-----|-----|
| 4 | Survives restarts | Notifications loaded from Postgres on startup |
| 5 | Fully async | `asyncpg` replaces `psycopg2` + thread |
| 6 | Structured logging | `logging` module with file rotation |

### Flow
```
INSERT into Postgres
  → trigger → pg_notify
  → asyncpg on_notify callback (async, no thread)
  → pushes directly to SSE clients + in-memory log
  → notify.py CLI receives it instantly
```

### CLI monitor
```bash
uv run python notify.py
uv run python notify.py --url http://localhost:8001
```

### Test with raw SQL
```sql
INSERT INTO notifications (notification) VALUES ('Hello from psql!');
```
""",
    version="5.0.0",
    lifespan=lifespan,
)


# ──────────────────────────────────────────────
# NOTIFICATION ROUTES
# ──────────────────────────────────────────────
@app.get("/notifications/", tags=["Notifications"])
def list_notifications():
    """List all notifications in the database."""
    db   = SessionLocal()
    rows = db.query(Notification).all()
    db.close()
    return [{"id": r.id, "notification": r.notification} for r in rows]


@app.post("/notifications/", status_code=201, tags=["Notifications"])
def add_notification(payload: NotificationCreate):
    """Add a notification — Postgres trigger fires NOTIFY instantly."""
    db  = SessionLocal()
    row = Notification(notification=payload.notification)
    db.add(row)
    db.commit()
    db.refresh(row)
    db.close()
    log.info(f"Notification added via API: id={row.id} | '{row.notification}'")
    return {"id": row.id, "notification": row.notification}


@app.delete("/notifications/{notification_id}", tags=["Notifications"])
def delete_notification(notification_id: int):
    """Delete a notification by ID."""
    db  = SessionLocal()
    row = db.query(Notification).filter(Notification.id == notification_id).first()
    if not row:
        db.close()
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(row)
    db.commit()
    db.close()
    log.info(f"Notification deleted: id={notification_id}")
    return {"message": f"Notification {notification_id} deleted"}


# ──────────────────────────────────────────────
# SSE STREAM
# ──────────────────────────────────────────────
@app.get("/webhook/stream", tags=["Webhook"])
async def webhook_stream(request: Request):
    """
    📡 SSE stream — connect here to receive notifications in real-time.
    Zero polling. Pure server-push.
    """
    q = sse_manager.add_client()

    async def event_generator():
        yield "event: connected\ndata: {\"status\": \"connected\"}\n\n"
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(q.get(), timeout=30.0)
                    yield f"event: notification\ndata: {json.dumps(data)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            sse_manager.remove_client(q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":     "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/webhook/notifications", tags=["Webhook"])
def get_received_notifications():
    """In-memory snapshot of recent notifications (newest first)."""
    return {
        "total":         len(received_notifications),
        "capped_at":     MAX_NOTIFICATIONS,
        "notifications": list(reversed(received_notifications)),
    }


@app.delete("/webhook/notifications", tags=["Webhook"])
def clear_webhook_log():
    """Clear the in-memory notification log."""
    received_notifications.clear()
    log.info("In-memory notification log cleared.")
    return {"message": "Cleared."}


# ──────────────────────────────────────────────
# ROOT
# ──────────────────────────────────────────────
@app.get("/", tags=["Info"])
def root():
    return {
        "docs":       f"http://127.0.0.1:{PORT}/docs",
        "sse_stream": f"http://127.0.0.1:{PORT}/webhook/stream",
        "mechanism":  "Postgres INSERT → asyncpg NOTIFY → direct SSE push",
        "polling":    False,
        "cli":        "uv run python notify.py",
    }
