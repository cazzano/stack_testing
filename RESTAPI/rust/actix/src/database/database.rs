use sqlx::{
    sqlite::{SqliteConnectOptions, SqlitePoolOptions},
    SqlitePool,
};
use std::path::Path;

pub async fn init_db(db_path: &str) -> Result<SqlitePool, sqlx::Error> {
    let path = Path::new(db_path);

    // Ensure parent directory exists on all platforms (Linux, Windows, Android).
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            std::fs::create_dir_all(parent).map_err(|e| {
                sqlx::Error::Io(std::io::Error::new(
                    e.kind(),
                    format!("Failed to create db directory '{}': {}", parent.display(), e),
                ))
            })?;
        }
    }

    // Build connection options using the path directly — avoids malformed
    // "sqlite:////absolute/path" URLs that occur when prepending "sqlite:///"
    // to an already-absolute path.
    let opts = SqliteConnectOptions::new()
        .filename(path)
        .create_if_missing(true)
        .foreign_keys(true);

    let pool = SqlitePoolOptions::new()
        .max_connections(5)
        .connect_with(opts)
        .await?;

    // Run SQLx migrations
    sqlx::migrate!("./migrations").run(&pool).await?;

    Ok(pool)
}
