//! JWT Bearer authentication middleware.
//!
//! Validates the `Authorization: Bearer <token>` header, decodes the HS256 JWT,
//! and checks that the token exists in the `tokens` table with `revoke = 0`.
//! On success the decoded `JwtClaims` struct is inserted into request extensions
//! so that route handlers can read it with `req.extensions().get::<JwtClaims>()`.

use actix_web::{
    body::EitherBody,
    dev::{Service, ServiceRequest, ServiceResponse, Transform},
    HttpMessage, HttpResponse, Error,
};
use jsonwebtoken::{decode, Algorithm, DecodingKey, Validation};
use serde::{Deserialize, Serialize};
use sqlx::SqlitePool;
use std::{
    future::Future,
    pin::Pin,
    rc::Rc,
};

/// The JWT claims shape matching what `auth_core::token` issues.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JwtClaims {
    pub user_id: String,
    pub username: String,
    pub role_type: String,
    pub clinic_id: Option<String>,
    pub exp: u64,
}

/// Error response shape for 401 responses.
#[derive(Serialize)]
struct AuthError {
    error: &'static str,
    message: String,
}

fn unauthorized(msg: &str) -> HttpResponse {
    HttpResponse::Unauthorized().json(AuthError {
        error: "unauthorized",
        message: msg.to_string(),
    })
}

// ── Middleware factory ────────────────────────────────────────────────────────

/// Routes that should be protected by JWT validation.
/// Any route **not** in this list will pass through without auth checks.
const PROTECTED_PREFIXES: &[&str] = &[
    "/auth/logout",
];

pub struct JwtAuthMiddleware;

impl<S, B> Transform<S, ServiceRequest> for JwtAuthMiddleware
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: actix_web::body::MessageBody + 'static,
{
    type Response = ServiceResponse<EitherBody<B>>;
    type Error = Error;
    type InitError = ();
    type Transform = JwtAuthMiddlewareService<S>;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Transform, Self::InitError>>>>;

    fn new_transform(&self, service: S) -> Self::Future {
        Box::pin(async move {
            Ok(JwtAuthMiddlewareService {
                service: Rc::new(service),
            })
        })
    }
}

// ── Middleware service ────────────────────────────────────────────────────────

pub struct JwtAuthMiddlewareService<S> {
    service: Rc<S>,
}

impl<S, B> Service<ServiceRequest> for JwtAuthMiddlewareService<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: actix_web::body::MessageBody + 'static,
{
    type Response = ServiceResponse<EitherBody<B>>;
    type Error = Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>>>>;

    actix_web::dev::forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let path = req.path().to_string();
        let is_protected = PROTECTED_PREFIXES.iter().any(|p| path.starts_with(p));

        if !is_protected {
            let service = Rc::clone(&self.service);
            return Box::pin(async move {
                service.call(req).await.map(|res| res.map_into_left_body())
            });
        }

        // Extract "Authorization: Bearer <token>"
        let auth_header = req
            .headers()
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .map(|s| s.to_string());

        let raw_token = match auth_header {
            Some(ref h) if h.starts_with("Bearer ") => h[7..].trim().to_string(),
            _ => {
                let (req, _pl) = req.into_parts();
                let resp = unauthorized("Missing or malformed Authorization header.")
                    .map_into_right_body();
                return Box::pin(async move {
                    Ok(ServiceResponse::new(req, resp))
                });
            }
        };

        let service = Rc::clone(&self.service);
        Box::pin(async move {
            let pool = req
                .app_data::<actix_web::web::Data<SqlitePool>>()
                .map(|d| d.clone());

            // ── Decode JWT ───────────────────────────────────────────────────
            let jwt_secret = std::env::var("JWT_SECRET")
                .unwrap_or_else(|_| "kcs-default-jwt-secret-change-me".into());

            let mut validation = Validation::new(Algorithm::HS256);
            validation.validate_exp = true;

            let claims = decode::<JwtClaims>(
                &raw_token,
                &DecodingKey::from_secret(jwt_secret.as_bytes()),
                &validation,
            );

            let claims = match claims {
                Ok(td) => td.claims,
                Err(e) => {
                    let (req, _pl) = req.into_parts();
                    let resp = unauthorized(&format!("Invalid token: {}", e)).map_into_right_body();
                    return Ok(ServiceResponse::new(req, resp));
                }
            };

            // ── Check revocation in DB ───────────────────────────────────────
            if let Some(pool) = pool {
                #[derive(sqlx::FromRow)]
                struct RevokeRow { revoke: i64 }

                let row: Option<RevokeRow> = sqlx::query_as::<_, RevokeRow>(
                    "SELECT revoke FROM tokens WHERE token = ?1 LIMIT 1",
                )
                .bind(&raw_token)
                .fetch_optional(pool.get_ref())
                .await
                .unwrap_or(None);

                match row {
                    Some(r) if r.revoke == 1 => {
                        let (req, _pl) = req.into_parts();
                        let resp = unauthorized("Token has been revoked.").map_into_right_body();
                        return Ok(ServiceResponse::new(req, resp));
                    }
                    None => {
                        let (req, _pl) = req.into_parts();
                        let resp = unauthorized("Token not recognized.").map_into_right_body();
                        return Ok(ServiceResponse::new(req, resp));
                    }
                    _ => {}
                }
            }

            // ── Inject claims into request extensions ─────────────────────────
            req.extensions_mut().insert(claims);

            service.call(req).await.map(|res| res.map_into_left_body())
        })
    }
}
