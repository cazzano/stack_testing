use actix_web::{post, web, HttpMessage, HttpRequest, HttpResponse};
use serde::{Deserialize, Serialize};
use sqlx::SqlitePool;
use utoipa::ToSchema;
use uuid::Uuid;

use auth_core::{
    decrypt::decrypt_payload,
    hmac_verify::verify as hmac_verify,
    credentials::parse as parse_credentials,
    password::verify as password_verify,
    checks::{verify_profile, verify_company},
    token::issue as token_issue,
    UserRecord, JwtConfig, CompanyRecord,
};

use crate::database::tokens::{insert_token, revoke_all_for_user};
use crate::shared::middleware::auth_middleware::JwtClaims;


// ── Request / Response Schemas ────────────────────────────────────────────────

/// Login request body — contains AES-GCM encrypted credentials
/// sent by the frontend using the 90-second epoch protocol.
#[derive(Debug, Deserialize, ToSchema)]
pub struct LoginRequest {
    /// Base64-encoded AES-256-GCM ciphertext (12-byte IV prepended)
    pub payload: String,
    /// Hex-encoded HMAC-SHA256 signature of the payload
    pub signature: String,
}

/// Successful login response
#[derive(Debug, Serialize, ToSchema)]
pub struct LoginResponse {
    /// JWT access token (HS256)
    pub access_token: String,
    /// Token type, always "Bearer"
    pub token_type: String,
}

/// Generic error response
#[derive(Debug, Serialize, ToSchema)]
pub struct AuthErrorResponse {
    /// Machine-readable error code
    pub error: String,
    /// Human-readable description
    pub message: String,
}

/// Successful logout response
#[derive(Debug, Serialize, ToSchema)]
pub struct LogoutResponse {
    /// How many token records were revoked
    pub revoked_count: u64,
    /// Confirmation message
    pub message: String,
}


// ── Database row helpers ───────────────────────────────────────────────────────

#[derive(Debug, sqlx::FromRow)]
struct UserRow {
    id: String,
    username: String,
    password: String,
    role: String,
    status: String,
    clinic_id: Option<String>,
    deleted_at: Option<String>,
}

#[derive(Debug, sqlx::FromRow)]
struct ClinicRow {
    id: String,
    deleted_at: Option<String>,
}

// ── Handlers ──────────────────────────────────────────────────────────────────

/// Login — issue a JWT access token
///
/// Accepts an AES-256-GCM encrypted payload and HMAC-SHA256 signature
/// constructed by the frontend using the 90-second rotating epoch protocol.
/// On success the token is stored in the `tokens` table with `revoke = 0`.
#[utoipa::path(
    post,
    path = "/auth/login",
    tag = "Auth",
    request_body = LoginRequest,
    responses(
        (status = 200, description = "Login successful — JWT returned", body = LoginResponse),
        (status = 400, description = "Missing or malformed payload/signature", body = AuthErrorResponse),
        (status = 401, description = "Invalid credentials, wrong password, or inactive account", body = AuthErrorResponse),
        (status = 404, description = "User not found", body = AuthErrorResponse),
        (status = 500, description = "Internal server error", body = AuthErrorResponse),
    )
)]
#[post("/auth/login")]
pub async fn login(
    pool: web::Data<SqlitePool>,
    body: web::Json<LoginRequest>,
) -> HttpResponse {
    let payload   = body.payload.trim();
    let signature = body.signature.trim();

    if payload.is_empty() || signature.is_empty() {
        return HttpResponse::BadRequest().json(AuthErrorResponse {
            error: "missing_fields".into(),
            message: "Both `payload` and `signature` are required.".into(),
        });
    }

    // ── Step 1: Verify HMAC ──────────────────────────────────────────────────
    if !hmac_verify(payload, signature) {
        return HttpResponse::Unauthorized().json(AuthErrorResponse {
            error: "hmac_invalid".into(),
            message: "Request signature is invalid. Ensure your client clock is within 90 seconds of server time.".into(),
        });
    }

    // ── Step 2: Decrypt AES-GCM payload ─────────────────────────────────────
    let decrypted = match decrypt_payload(payload) {
        Some(s) => s,
        None => {
            return HttpResponse::Unauthorized().json(AuthErrorResponse {
                error: "decrypt_failed".into(),
                message: "Payload could not be decrypted.".into(),
            });
        }
    };

    // ── Step 3: Parse credentials ────────────────────────────────────────────
    let (username_opt, _phone_opt, submitted_hash) = match parse_credentials(&decrypted) {
        Ok(v) => v,
        Err(e) => {
            return HttpResponse::BadRequest().json(AuthErrorResponse {
                error: format!("parse_failed: {}", e),
                message: "Could not parse decrypted credentials.".into(),
            });
        }
    };

    let username = match username_opt {
        Some(u) => u,
        None => {
            return HttpResponse::BadRequest().json(AuthErrorResponse {
                error: "missing_username".into(),
                message: "No username found in credentials.".into(),
            });
        }
    };

    // ── Step 4: Fetch user from database ─────────────────────────────────────
    let user_row: Option<UserRow> = sqlx::query_as::<_, UserRow>(
        r#"SELECT id, username, password, role, status, clinic_id, deleted_at
           FROM users WHERE username = ?1 LIMIT 1"#,
    )
    .bind(&username)
    .fetch_optional(pool.get_ref())
    .await
    .unwrap_or(None);

    let user_row = match user_row {
        Some(r) => r,
        None => {
            return HttpResponse::NotFound().json(AuthErrorResponse {
                error: "user_not_found".into(),
                message: "No account found with that username.".into(),
            });
        }
    };

    // ── Step 5: Build auth_core UserRecord & validate ─────────────────────────
    let user_record = UserRecord {
        id: user_row.id.clone(),
        username: user_row.username.clone(),
        stored_password_hash: user_row.password.clone(),
        role: user_row.role.clone(),
        is_deleted: user_row.deleted_at.is_some(),
    };

    if let Err(e) = password_verify(&submitted_hash, &user_record) {
        return HttpResponse::Unauthorized().json(AuthErrorResponse {
            error: e.into(),
            message: "Invalid credentials.".into(),
        });
    }

    // ── Step 6: Profile (user status) check ──────────────────────────────────
    let is_super_admin = user_row.role.eq_ignore_ascii_case("super_admin");

    if !is_super_admin {
        let profile = auth_core::ProfileRecord {
            exists: true,
            is_deleted: user_row.deleted_at.is_some(),
            status: user_row.status.to_uppercase(),
        };
        if let Err(e) = verify_profile(Some(&profile)) {
            return HttpResponse::Unauthorized().json(AuthErrorResponse {
                error: e.into(),
                message: "Account is inactive or deleted.".into(),
            });
        }
    }

    // ── Step 7: Clinic check (company) ───────────────────────────────────────
    let company_record: Option<CompanyRecord> = if !is_super_admin {
        if let Some(ref clinic_id) = user_row.clinic_id {
            let clinic_row: Option<ClinicRow> = sqlx::query_as::<_, ClinicRow>(
                r#"SELECT id, deleted_at FROM clinics WHERE id = ?1 LIMIT 1"#,
            )
            .bind(clinic_id)
            .fetch_optional(pool.get_ref())
            .await
            .unwrap_or(None);

            match clinic_row {
                Some(c) => Some(CompanyRecord {
                    exists: true,
                    is_deleted: c.deleted_at.is_some(),
                    status: "ACTIVE".into(), // clinics table has no status column — present = ACTIVE
                }),
                None => Some(CompanyRecord {
                    exists: false,
                    is_deleted: false,
                    status: "INACTIVE".into(),
                }),
            }
        } else {
            None // no clinic — skip company check
        }
    } else {
        None
    };

    if !is_super_admin {
        if let Err(e) = verify_company(company_record.as_ref()) {
            return HttpResponse::Unauthorized().json(AuthErrorResponse {
                error: e.into(),
                message: "Associated clinic is inactive or deleted.".into(),
            });
        }
    }

    // ── Step 8: Issue JWT ─────────────────────────────────────────────────────
    let jwt_secret = std::env::var("JWT_SECRET").unwrap_or_else(|_| "kcs-default-jwt-secret-change-me".into());
    let jwt_expiry: u64 = std::env::var("JWT_EXPIRY_MINUTES")
        .unwrap_or_else(|_| "1440".into())
        .parse()
        .unwrap_or(1440);

    let jwt_cfg = JwtConfig {
        secret: jwt_secret,
        algorithm: "HS256".into(),
        expiry_minutes: jwt_expiry,
    };

    let access_token = match token_issue(&user_record, user_row.clinic_id.clone(), &jwt_cfg) {
        Ok(t) => t,
        Err(e) => {
            log::error!("JWT issue error: {}", e);
            return HttpResponse::InternalServerError().json(AuthErrorResponse {
                error: format!("jwt_failed: {}", e),
                message: "Failed to generate access token.".into(),
            });
        }
    };

    // ── Step 9: Store token in DB ─────────────────────────────────────────────
    let token_id = Uuid::new_v4().to_string();
    if let Err(e) = insert_token(pool.get_ref(), &token_id, &access_token, &user_row.id).await {
        log::error!("Failed to store token: {}", e);
        return HttpResponse::InternalServerError().json(AuthErrorResponse {
            error: "db_error".into(),
            message: "Failed to persist session token.".into(),
        });
    }

    HttpResponse::Ok().json(LoginResponse {
        access_token,
        token_type: "Bearer".into(),
    })
}

// ── Logout ────────────────────────────────────────────────────────────────────

/// Logout — revoke all tokens for the authenticated user
///
/// Requires a valid Bearer JWT in the `Authorization` header.
/// Sets `revoke = 1` on **every** token row for that user, invalidating all sessions.
#[utoipa::path(
    post,
    path = "/auth/logout",
    tag = "Auth",
    security(("bearer_auth" = [])),
    responses(
        (status = 200, description = "All tokens revoked successfully", body = LogoutResponse),
        (status = 401, description = "Missing or invalid/revoked token", body = AuthErrorResponse),
        (status = 500, description = "Internal server error", body = AuthErrorResponse),
    )
)]
#[post("/auth/logout")]
pub async fn logout(
    req: HttpRequest,
    pool: web::Data<SqlitePool>,
) -> HttpResponse {
    // The JWT middleware injects the validated claims as an extension.
    let claims = req.extensions().get::<JwtClaims>().cloned();

    let user_id = match claims {
        Some(c) => c.user_id,
        None => {
            return HttpResponse::Unauthorized().json(AuthErrorResponse {
                error: "unauthorized".into(),
                message: "Authentication required. Provide a valid Bearer token.".into(),
            });
        }
    };

    match revoke_all_for_user(pool.get_ref(), &user_id).await {
        Ok(count) => HttpResponse::Ok().json(LogoutResponse {
            revoked_count: count,
            message: format!("Successfully revoked {} token(s) for user.", count),
        }),
        Err(e) => {
            log::error!("Failed to revoke tokens: {}", e);
            HttpResponse::InternalServerError().json(AuthErrorResponse {
                error: "db_error".into(),
                message: "Failed to revoke tokens.".into(),
            })
        }
    }
}
