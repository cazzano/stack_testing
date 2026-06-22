use serde::Deserialize;
use std::env;
use std::path::PathBuf;

/// Expands tilde (`~`) to the user's home directory cross-platform.
/// Falls back to `/shared/data/` on Android or other platforms where home isn't found.
fn expand_tilde(path: &str) -> String {
    if !path.starts_with('~') {
        return path.to_string();
    }

    let home = dirs::home_dir().or_else(|| {
        // Android fallback: try /shared/data/ or /data/
        #[cfg(target_os = "android")]
        {
            std::env::var("ANDROID_DATA")
                .ok()
                .map(|p| PathBuf::from(p).join("data"))
        }
        #[cfg(not(target_os = "android"))]
        None
    });

    match home {
        Some(home_path) => {
            let remainder = &path[1..];
            let remainder = remainder.trim_start_matches('/');
            if remainder.is_empty() {
                home_path.to_string_lossy().to_string()
            } else {
                home_path.join(remainder).to_string_lossy().to_string()
            }
        }
        None => {
            // Ultimate fallback - use a reasonable default
            let fallback = PathBuf::from("/shared/data");
            std::fs::create_dir_all(&fallback).ok();
            let remainder = path.trim_start_matches('~');
            let remainder = remainder.trim_start_matches('/');
            if remainder.is_empty() {
                fallback.to_string_lossy().to_string()
            } else {
                fallback.join(remainder).to_string_lossy().to_string()
            }
        }
    }
}

#[derive(Debug, Clone, Deserialize)]
pub struct AppConfig {
    pub db_path: String,
    pub host: String,
    pub port: u16,
    pub cors_origins: String,
}

impl AppConfig {
    pub fn new() -> Self {
        // Load .env from the backend crate directory (baked at compile time).
        // This works whether the binary is run standalone or spawned by Tauri.
        // dotenv respects existing env vars — it won't override sql_db_path set by Tauri.
        let manifest_env = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(".env");
        if manifest_env.exists() {
            dotenv::from_path(&manifest_env).ok();
        } else {
            dotenv::dotenv().ok();
        }

        // sql_db_path is set by Tauri (lib.rs) to app_data_dir/database.db before
        // spawning this server. The fallback below is only used when running standalone.
        let db_path =
            env::var("sql_db_path").unwrap_or_else(|_| "database.db".to_string());
        
        let path = if db_path.starts_with("sqlite:///") {
            db_path.strip_prefix("sqlite:///").unwrap_or(&db_path).to_string()
        } else {
            db_path
        };
        
        let db_path = expand_tilde(&path);

        let cors_origins_default = "http://localhost:3000,http://localhost:5173,http://localhost:4173,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:4173,http://127.0.0.1:8543,http://localhost:8543,tauri://localhost,http://tauri.localhost,https://tauri.localhost,tauri.localhost".to_string();

        Self {
            db_path,
            host: env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string()),
            port: env::var("app_port")
                .unwrap_or_else(|_| "8543".to_string())
                .parse()
                .unwrap_or(8543),
            cors_origins: env::var("CORS_ORIGINS").unwrap_or_else(|_| cors_origins_default),
        }
    }
}

impl Default for AppConfig {
    fn default() -> Self {
        Self::new()
    }
}
