"""
TRUE Webhook — PostgreSQL LISTEN/NOTIFY + SSE
=============================================
Only one endpoint: GET /webhook/stream
Everything else is gone. Pure webhook.

Flow:
  Postgres INSERT
    → pg trigger fires NOTIFY instantly
    → asyncpg on_notify callback (pure async, no thread)
    → pushes directly to all SSE clients
    → notify.py CLI receives it instantly
"""

import asyncio
import json
import logging
import logging.handlers
import os
from contextlib import asynccontextmanager
from datetime import datetime

import asyncpg
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import Column, Integer, Text, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
PORT        = int(os.getenv("PORT", 8000))
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = int(os.getenv("DB_PORT", 5432))
DB_NAME     = os.getenv("DB_NAME", "notify")
DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
LOG_FILE    = "webhook.log"

ASYNCPG_DSN    = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
def setup_logging():
    logger = logging.getLogger("webhook")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
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
# DATABASE — only used to create table + trigger
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


# ──────────────────────────────────────────────
# ASYNC POSTGRES LISTENER
# ──────────────────────────────────────────────
async def pg_listener():
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
                await sse_manager.broadcast(entry)

            await conn.add_listener("new_notification", on_notify)

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
            log.error(f"Unexpected error: {e}. Retrying in {backoff}s...")
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
# LIFESPAN
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_db()
    listener_task = asyncio.create_task(pg_listener())
    log.info(f"App ready — Webhook stream: http://127.0.0.1:{PORT}/webhook/stream")
    yield
    listener_task.cancel()
    await asyncio.gather(listener_task, return_exceptions=True)
    log.info("Shutdown complete.")


# ──────────────────────────────────────────────
# APP
# ──────────────────────────────────────────────
app = FastAPI(
    title="True Notification Webhook",
    description="""
## 🔔 True Webhook — PostgreSQL LISTEN/NOTIFY + SSE

One endpoint. No REST APIs. Pure webhook.

### Flow
```
INSERT into notifications
  → Postgres trigger fires NOTIFY instantly
  → asyncpg on_notify callback wakes (pure async)
  → pushes directly to all SSE clients
  → notify.py receives instantly
```

### Insert a notification
```sql
INSERT INTO notifications (notification) VALUES ('hello!');
```

### Watch live
```bash
uv run python notify.py
```
""",
    version="6.0.0",
    lifespan=lifespan,
)


# ──────────────────────────────────────────────
# THE ONLY ENDPOINT — the webhook
# ──────────────────────────────────────────────
@app.get("/webhook/stream", tags=["Webhook"])
async def webhook_stream(request: Request):
    """
    🪝 The webhook.

    Connect here and leave the connection open.
    The server pushes every new notification the instant
    Postgres fires NOTIFY — zero polling, pure server-push.
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
