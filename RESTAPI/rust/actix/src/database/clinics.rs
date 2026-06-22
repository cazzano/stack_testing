use sqlx::SqlitePool;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Clinic {
    pub id: String,
    pub name: String,
    pub created_at: Option<String>,
}

pub async fn upsert_clinic(pool: &SqlitePool, clinic: &Clinic) -> Result<(), sqlx::Error> {
    sqlx::query(
        r#"INSERT INTO clinics (id, name)
           VALUES (?1, ?2)
           ON CONFLICT(id) DO UPDATE SET
               name = ?2"#,
    )
    .bind(&clinic.id)
    .bind(&clinic.name)
    .execute(pool)
    .await?;
    Ok(())
}
