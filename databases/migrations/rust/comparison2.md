# Alembic vs Diesel — The "3 Legendary Steps"

Alembic's loop is:
1. Edit `schema.py` (the model)
2. `alembic revision --autogenerate -m "..."` (generate migration by diffing)
3. `alembic upgrade head` (apply to DB)

Diesel **inverts this entirely**. There is no "edit the model first" step, because in Diesel the model file (`schema.rs`) is not hand-written — it's generated output. Here's how Diesel's loop actually maps.

## The 3 steps, side by side

| Step | Alembic | Diesel |
|---|---|---|
| **1. Define the change** | Edit `schema.py` — add/change a SQLAlchemy model class | `diesel migration generate add_lock_file_column` — creates an empty `up.sql` / `down.sql` pair, then **you hand-write the SQL** |
| **2. Generate** | `alembic revision --autogenerate -m "..."` — diffs `schema.py` against the live DB and writes the migration file for you | *(nothing — there is no generation step; you already wrote the SQL in step 1)* |
| **3. Apply** | `alembic upgrade head` — runs the migration SQL against the DB | `diesel migration run` — runs your SQL **and** regenerates `src/schema.rs` from the resulting DB via `print-schema` |

So Diesel collapses Alembic's 3 steps into 2, but the "generation" intelligence is on the opposite end:

- Alembic generates **the migration** from **the model**.
- Diesel generates **the model** (`schema.rs`) from **the migration result** (the live DB after running your SQL).

## Walking through a real example

Say you want to add `lock_file TEXT` to `clinic_devices`.

**Alembic**
```bash
# 1. Edit app/database/schema.py
class ClinicDevices(Base, TimestampMixin):
    ...
    lock_file = Column(Text, nullable=True)

# 2. Generate
alembic revision --autogenerate -m "add lock_file column to clinic_devices"
# -> writes alembic/versions/b54cdfa6cefa_add_lock_file_column_to_clinic_devices.py
#    containing op.add_column('clinic_devices', sa.Column('lock_file', sa.Text(), nullable=True))

# 3. Apply
alembic upgrade head
```

**Diesel**
```bash
# 1. Define the change — create migration skeleton
diesel migration generate add_lock_file_column_to_clinic_devices
# -> creates migrations/2026-06-16-.../up.sql and down.sql (both empty)

# you write up.sql by hand:
#   ALTER TABLE clinic_devices ADD COLUMN lock_file TEXT;
# and down.sql by hand:
#   ALTER TABLE clinic_devices DROP COLUMN lock_file;

# 3. Apply (also regenerates schema.rs)
diesel migration run
# -> runs up.sql against the DB
# -> rewrites src/schema.rs to include:
#    lock_file -> Nullable<Text>,
```

There's no Diesel equivalent of step 2 — the "autogenerate a diff" intelligence simply doesn't exist on the schema → migration side. The SQL is always yours.

## What you gain / lose by NOT having step 2

| | Alembic | Diesel |
|---|---|---|
| Writing the DDL | Mostly automatic, occasionally needs manual correction (as seen repeatedly with `clinic_rules.api_key` defaults in this project) | Always manual — you write real SQL every time |
| Risk of autogenerate guessing wrong (e.g. server defaults, computed columns) | Yes — this has bitten this project's migration history multiple times | N/A — nothing to guess, because nothing is auto-derived from a model |
| `schema.rs` staying in sync with DB | N/A (Python models are the source, no separate generated file) | Guaranteed — `schema.rs` is regenerated every `migration run`, so it can never drift from the DB |
| Compile-time safety | None — a typo in `schema.py` only fails at query runtime | High — Diesel's macros build types from `schema.rs`; a renamed/dropped column breaks the build everywhere it's used |

## Rollback comparison

| | Alembic | Diesel |
|---|---|---|
| One step back | `alembic downgrade -1` | `diesel migration revert` (runs `down.sql` of the last migration, also re-regenerates `schema.rs`) |
| To a specific revision | `alembic downgrade <rev_id>` | No direct "jump to revision" — revert repeatedly or `diesel migration redo` for revert+reapply of the last one |

## Multi-database (Postgres + SQLite)

Both tools need the same care here: Postgres-only DDL (e.g. `gen_random_uuid()`, computed/generated columns, the `clinic_rules.api_key` random-string default seen in `schema.py`) has no SQLite equivalent. Alembic handles this by writing dialect-aware migration code if needed (or you maintain separate migration trees). Diesel handles it the same way — your hand-written `up.sql`/`down.sql` would need separate versions per backend, since Diesel doesn't abstract dialect differences in raw SQL migrations the way an ORM-level DSL might.

## Bottom line

- **Alembic**: "describe the desired end state (`schema.py`), get the change computed for you." Step 2 (autogenerate) is real automation, with real edge-case risk.
- **Diesel**: "describe the change yourself (SQL), get the end state (`schema.rs`) computed for you." The automation is on the *output* side, not the *input* side — and it's a much smaller, much more reliable piece of automation (a straight `print-schema` against the DB, nothing to guess).

If your team's mental model is "I think in terms of the model, not the SQL," Diesel will feel like a step backwards from Alembic. If your team is comfortable writing SQL and wants the compiler to catch every place a schema change breaks the codebase, Diesel's tradeoff is a good one — you just won't get the "autogenerate did 80% of the work" feeling Alembic gives you.
