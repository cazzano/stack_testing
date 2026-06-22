use sqlx::SqlitePool;

#[derive(Debug, Clone, sqlx::FromRow)]
pub struct TokenRow {
    pub id: String,
    pub token: String,
    pub revoke: i64,
    pub user_id: String,
}

/// Insert a new token record with revoke = 0.
pub async fn insert_token(pool: &SqlitePool, id: &str, token: &str, user_id: &str) -> Result<(), sqlx::Error> {
    sqlx::query(
        r#"INSERT INTO tokens (id, token, revoke, user_id) VALUES (?1, ?2, 0, ?3)"#,
    )
    .bind(id)
    .bind(token)
    .bind(user_id)
    .execute(pool)
    .await?;
    Ok(())
}

/// Revoke ALL tokens for a given user_id (sets revoke = 1).
pub async fn revoke_all_for_user(pool: &SqlitePool, user_id: &str) -> Result<u64, sqlx::Error> {
    let result = sqlx::query(
        r#"UPDATE tokens SET revoke = 1 WHERE user_id = ?1"#,
    )
    .bind(user_id)
    .execute(pool)
    .await?;
    Ok(result.rows_affected())
}

/// Find a token row by the raw JWT string. Returns None if not found.
pub async fn find_by_token(pool: &SqlitePool, token: &str) -> Result<Option<TokenRow>, sqlx::Error> {
    let row = sqlx::query_as::<_, TokenRow>(
        r#"SELECT id, token, revoke, user_id FROM tokens WHERE token = ?1"#,
    )
    .bind(token)
    .fetch_optional(pool)
    .await?;
    Ok(row)
}
