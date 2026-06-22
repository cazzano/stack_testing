use actix_web::{web, HttpResponse};
use utoipa::OpenApi;
use utoipa::openapi::security::{HttpAuthScheme, HttpBuilder, SecurityScheme};
use utoipa::Modify;
use utoipa_swagger_ui::SwaggerUi;

use crate::router::auth::{login, logout, LoginRequest, LoginResponse, LogoutResponse, AuthErrorResponse};
use crate::shared::middleware::auth_middleware::JwtAuthMiddleware;

// ── OpenAPI Security Addon ────────────────────────────────────────────────────

struct SecurityAddon;

impl Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        if let Some(components) = openapi.components.as_mut() {
            components.add_security_scheme(
                "bearer_auth",
                SecurityScheme::Http(
                    HttpBuilder::new()
                        .scheme(HttpAuthScheme::Bearer)
                        .bearer_format("JWT")
                        .build(),
                ),
            );
        }
    }
}

// ── OpenAPI Document ──────────────────────────────────────────────────────────

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::router::auth::login,
        crate::router::auth::logout,
    ),
    components(
        schemas(
            LoginRequest,
            LoginResponse,
            LogoutResponse,
            AuthErrorResponse,
        )
    ),
    modifiers(&SecurityAddon),
    tags(
        (name = "Auth", description = "Authentication — login, logout, and token management"),
    ),
    info(
        title = "KCS Clinic Management API",
        version = "1.0.0",
        description = "REST API for Kairo Clinic Management System. Use the **Authorize** button to paste a JWT Bearer token for protected endpoints.",
        contact(name = "KairoSys", email = "support@kairosys.com"),
        license(name = "Proprietary"),
    ),
)]
pub struct ApiDoc;

// ── Route Registration ────────────────────────────────────────────────────────

pub fn register_routes(cfg: &mut web::ServiceConfig) {
    cfg
        // Root health check
        .route("/", web::get().to(root))

        // Auth routes with JWT middleware scoped to /auth
        .service(
            web::scope("/auth")
                .wrap(JwtAuthMiddleware)
                .service(login)
                .service(logout),
        )

        // Swagger UI
        .service(
            SwaggerUi::new("/swagger-ui/{_:.*}")
                .url("/api-docs/openapi.json", ApiDoc::openapi()),
        );
}

async fn root() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "ok",
        "message": "KCS Clinic Management Backend is running",
        "version": "1.0.0",
        "docs": "/swagger-ui/"
    }))
}
