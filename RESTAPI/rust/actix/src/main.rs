use actix_web::{get, App, HttpResponse, HttpServer, Responder};
use serde_json::json;

#[get("/api/hello")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().json(json!({
        "message": "hello hi"
    }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(hello)
    })
    .bind(("0.0.0.0", 6000))?
    .run()
    .await
}
