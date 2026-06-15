# Alembic vs sea-orm-migration

## 1. Core philosophy

| | Alembic | sea-orm-migration |
|---|---|---|
| Source of truth | `schema.py` (SQLAlchemy models) — migrations are *derived* from it | Migration files themselves — entities are *derived* from the DB after migrations run |
| Direction of generation | Model → Migration (autogenerate diff) | Migration → Entity (`sea-orm-cli generate entity`) |
| Migration content | Auto-written `op.xxx()` calls, reviewed/edited by hand | Hand-written `up()`/`down()` using SeaQuery's schema builder |
| Language | Python | Rust |

The key mental shift: in Alembic you edit the model and let the tool figure out the SQL diff. In sea-orm-migration you write the SQL-equivalent migration yourself (in Rust), then regenerate the model code from the result.

## 2. Project layout

**Alembic**
```
alembic/
  env.py
  script.py.mako
  versions/
    98e2e62055d9_initial_clinic_schema.py
    15cde1cb405c_add_server_default_for_ids.py
    ...
app/database/schema.py   <- the models, hand-edited
```

**sea-orm-migration**
```
migration/
  src/
    lib.rs              <- registers all migrations in order
    m20250101_000001_create_table.rs
    m20250102_000002_add_column.rs
    ...
src/entities/
  mod.rs
  users.rs              <- generated, not hand-edited
  clinics.rs
```

## 3. The day-to-day loop

**Alembic**
```bash
# 1. edit app/database/schema.py
# 2. generate migration by diffing models vs live DB
alembic revision --autogenerate -m "add lock_file column"
# 3. review/adjust the generated upgrade()/downgrade()
# 4. apply
alembic upgrade head
```

**sea-orm-migration**
```bash
# 1. create a new empty migration file
sea-orm-cli migrate generate add_lock_file_column
# 2. hand-write up()/down() using SeaQuery schema builder
# 3. apply
sea-orm-cli migrate up
# 4. regenerate entity structs from the new DB state
sea-orm-cli generate entity -o src/entities
```

Alembic: 1 manual step (edit model), 1 automated step (diff).
sea-orm: 1 manual step (write migration), 1 automated step (entity regen).

## 4. What a single migration looks like

**Alembic** (auto-generated, e.g. `1a0dbbfd5ee8_set_clinicrules_defaults.py`)
```python
def upgrade() -> None:
    op.alter_column('clinic_rules', 'rx_templates',
        existing_type=sa.INTEGER(),
        server_default=sa.text('10'),
        existing_nullable=True)

def downgrade() -> None:
    op.alter_column('clinic_rules', 'rx_templates',
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=True)
```

**sea-orm-migration** (hand-written equivalent)
```rust
#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(ClinicRules::Table)
                    .modify_column(
                        ColumnDef::new(ClinicRules::RxTemplates)
                            .integer()
                            .default(10),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(ClinicRules::Table)
                    .modify_column(
                        ColumnDef::new(ClinicRules::RxTemplates).integer(),
                    )
                    .to_owned(),
            )
            .await
    }
}
```

## 5. Revision chain / ordering

| | Alembic | sea-orm-migration |
|---|---|---|
| Ordering mechanism | `revision` / `down_revision` UUID-like IDs forming a linked list | Filename timestamp prefix (`mYYYYMMDD_HHMMSS_name.rs`), registered in order inside `lib.rs`'s `Migrator::migrations()` |
| Branch detection | `alembic heads` shows multiple heads if branched | No built-in branch detection — order is whatever you list in `lib.rs` |
| History inspection | `alembic history`, `alembic current` | `sea-orm-cli migrate status` |
| Tracking table | `alembic_version` | `seaql_migrations` |

## 6. Autogeneration capability

| Capability | Alembic (`--autogenerate`) | sea-orm |
|---|---|---|
| Detect new/removed tables | ✅ | ❌ (manual) |
| Detect new/removed columns | ✅ | ❌ (manual) |
| Detect type changes | ✅ (with `compare_type=True`) | ❌ (manual) |
| Detect server_default changes | ✅ (with `compare_server_default=True`), often needs manual fix anyway | ❌ (manual) |
| Pre-check "is DB in sync with models" | ✅ `alembic check` | ❌ (no equivalent) |
| Generate entity code from DB | N/A (models are hand-written) | ✅ `sea-orm-cli generate entity` |

This is the biggest practical gap: Alembic saves you from writing ~80% of routine DDL by diffing; sea-orm-migration does **not** — every `up()`/`down()` is hand-written Rust, even for a simple `ADD COLUMN`.

## 7. Rollback

| | Alembic | sea-orm-migration |
|---|---|---|
| Rollback one step | `alembic downgrade -1` | `sea-orm-cli migrate down` |
| Rollback to specific revision | `alembic downgrade <rev_id>` | `sea-orm-cli migrate down -n <count>` (count-based, not ID-based) |
| Reset everything | `alembic downgrade base` | `sea-orm-cli migrate fresh` / `migrate reset` |

## 8. Multi-database support (Postgres + SQLite)

| | Alembic | sea-orm-migration |
|---|---|---|
| Same migration files for both dialects | Mostly, but Postgres-specific things (`gen_random_uuid()`, `UUID` type, generated columns) won't run on SQLite without conditional logic | Same — SeaQuery abstracts common DDL, but dialect-specific features still need `if manager.get_database_backend() == ...` branches |
| Config | `alembic.ini` `sqlalchemy.url` per environment | `DATABASE_URL` env var consumed by `sea-orm-cli`, feature flags (`sqlx-postgres` / `sqlx-sqlite`) select the driver |

Neither tool magically makes Postgres-only features (computed columns, `gen_random_uuid()`, custom defaults via SQL expressions like the `clinic_rules.api_key` default in `schema.py`) portable to SQLite — both require dialect-aware branching in the migration code if you truly share one migration history across both DBs.

## 9. Bottom line

- **Alembic** = "describe the desired state, let the tool compute the change." Lower effort per change, but autogenerate output for non-trivial changes (defaults, computed columns) still needs manual correction — as seen repeatedly in this project's own migration history.
- **sea-orm-migration** = "describe the change directly, then regenerate the state." More manual per migration, but explicit and predictable — no risk of autogenerate silently getting a default or type wrong, because there's no autogenerate to begin with.

If the team's expectation is "edit one file and a correct migration appears," sea-orm-migration won't deliver that — Atlas (mentioned earlier) is closer to that promise but isn't natively wired into Rust ORMs. SeaORM remains the best *practical* fit for an actix-web + Postgres/SQLite stack, just with a different (more manual, more explicit) day-to-day rhythm than Alembic.
