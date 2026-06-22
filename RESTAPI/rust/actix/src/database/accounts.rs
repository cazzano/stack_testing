use sqlx::SqlitePool;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Account {
    pub id: String,
    pub username: String,
    pub role: String,
    pub status: String,
    #[serde(rename = "password_hash")]
    pub password: String,
    pub clinic_id: Option<String>,
    pub clinic_name: Option<String>,
    pub created_at: String,
    pub updated_at: Option<String>,
    pub deleted_at: Option<String>,
}

pub async fn upsert(pool: &SqlitePool, account: &Account) -> Result<(), sqlx::Error> {
    sqlx::query(
        r#"INSERT INTO users (id, username, password, role, status, clinic_id, created_at, updated_at, deleted_at)
           VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)
           ON CONFLICT(id) DO UPDATE SET
               username = ?2,
               password = ?3,
               role = ?4,
               status = ?5,
               clinic_id = ?6,
               updated_at = ?8,
               deleted_at = ?9"#,
    )
    .bind(&account.id)
    .bind(&account.username)
    .bind(&account.password)
    .bind(&account.role)
    .bind(&account.status)
    .bind(&account.clinic_id)
    .bind(&account.created_at)
    .bind(&account.updated_at)
    .bind(&account.deleted_at)
    .execute(pool)
    .await?;
    Ok(())
}

pub async fn soft_delete(pool: &SqlitePool, id: &str) -> Result<(), sqlx::Error> {
    sqlx::query(
        r#"UPDATE users SET deleted_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?1"#,
    )
    .bind(id)
    .execute(pool)
    .await?;
    Ok(())
}

pub async fn get_all(pool: &SqlitePool) -> Result<Vec<Account>, sqlx::Error> {
    let rows = sqlx::query_as::<_, AccountRow>(
        r#"SELECT id, username, password, role, status, clinic_id, created_at, updated_at, deleted_at
           FROM users WHERE deleted_at IS NULL"#,
    )
    .fetch_all(pool)
    .await?;

    Ok(rows
        .into_iter()
        .map(|r| Account {
            id: r.id,
            username: r.username,
            role: r.role,
            status: r.status,
            password: r.password,
            clinic_id: r.clinic_id,
            clinic_name: None,
            created_at: r.created_at,
            updated_at: r.updated_at,
            deleted_at: r.deleted_at,
        })
        .collect())
}

pub async fn get_clinic_name(pool: &SqlitePool, clinic_id: &str) -> Result<Option<String>, sqlx::Error> {
    let result: Option<(String,)> =
        sqlx::query_as("SELECT name FROM clinics WHERE id = ?1")
            .bind(clinic_id)
            .fetch_optional(pool)
            .await?;
    Ok(result.map(|r| r.0))
}

#[derive(Debug, sqlx::FromRow)]
struct AccountRow {
    id: String,
    username: String,
    password: String,
    role: String,
    status: String,
    clinic_id: Option<String>,
    created_at: String,
    updated_at: Option<String>,
    deleted_at: Option<String>,
}
