pub mod config;
pub mod database;
pub mod shared;
pub mod router;

use actix_cors::Cors;
use actix_web::{http::header, web, App, HttpResponse, HttpServer};
use log::info;
use sqlx::SqlitePool;
use std::io;

use crate::config::config::AppConfig;
use crate::database::database::init_db;
use crate::router::routes::register_routes;
use crate::shared::middleware::LoggingMiddleware;

/// Start the server with a pre-existing pool (shared with Tauri).
pub async fn run_server_with_pool(pool: SqlitePool, config: AppConfig) -> io::Result<()> {
    let _ = env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info")).try_init();

    info!("Starting Note Taking Application Server");
    info!("Database path: {}", config.db_path);
    info!("Database connection established");

    let bind_address = format!("{}:{}", config.host, config.port);
    info!("Starting server at {}", bind_address);

    HttpServer::new(move || {
        let cors = if config.cors_origins == "*" {
            Cors::default()
                .send_wildcard()
                .allowed_methods(vec!["GET", "POST", "PUT", "DELETE", "OPTIONS"])
                .allowed_headers(vec![
                    header::AUTHORIZATION,
                    header::ACCEPT,
                    header::CONTENT_TYPE,
                ])
                .max_age(3600)
        } else {
            let origins: Vec<&str> = config.cors_origins.split(",").collect();
            let mut cors = Cors::default()
                .allowed_methods(vec!["GET", "POST", "PUT", "DELETE", "OPTIONS"])
                .allowed_headers(vec![
                    header::AUTHORIZATION,
                    header::ACCEPT,
                    header::CONTENT_TYPE,
                ])
                .allowed_header(header::ACCESS_CONTROL_ALLOW_ORIGIN)
                .max_age(3600);

            for origin in origins {
                cors = cors.allowed_origin(origin);
            }

            cors
        };

        App::new()
            .wrap(LoggingMiddleware)
            .wrap(cors)
            .app_data(web::Data::new(pool.clone()))
            .app_data(web::JsonConfig::default().error_handler(|err, _req| {
                let detail = err.to_string();
                log::error!("JSON Deserialization Error: {}", detail);
                actix_web::error::InternalError::from_response(
                    err,
                    HttpResponse::BadRequest().json(serde_json::json!({
                        "error": "Bad Request",
                        "detail": detail
                    })),
                )
                .into()
            }))
            .configure(register_routes)
    })
    .bind(&bind_address)?
    .run()
    .await
}

/// Start the server with its own pool (backwards-compatible entry point).
pub async fn run_server() -> io::Result<()> {
    let config = AppConfig::new();
    let pool = init_db(&config.db_path)
        .await
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;
    run_server_with_pool(pool, config).await
}
