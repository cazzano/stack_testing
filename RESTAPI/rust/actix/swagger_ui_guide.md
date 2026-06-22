# utoipa + Swagger UI — Complete Integration Guide for actix-web

> Auto-generate interactive OpenAPI 3.0 documentation from your Rust code.  
> No manual YAML. No separate doc files. Just annotate and run.

---

## Table of Contents

1. [What You're Setting Up](#1-what-youre-setting-up)
2. [Cargo.toml — Dependencies](#2-cargotoml--dependencies)
3. [Project Structure](#3-project-structure)
4. [Step 1 — Define Your Schemas with `ToSchema`](#4-step-1--define-your-schemas-with-toschema)
5. [Step 2 — Annotate Your Route Handlers](#5-step-2--annotate-your-route-handlers)
6. [Step 3 — Create the OpenAPI Document](#6-step-3--create-the-openapi-document)
7. [Step 4 — Mount Swagger UI in actix-web](#7-step-4--mount-swagger-ui-in-actix-web)
8. [Full Working Example — CRUD API](#8-full-working-example--crud-api)
9. [Query Parameters with `IntoParams`](#9-query-parameters-with-intoparams)
10. [JWT Bearer Auth in Swagger UI](#10-jwt-bearer-auth-in-swagger-ui)
11. [API Tags and Grouping](#11-api-tags-and-grouping)
12. [Multiple Response Types & Error Bodies](#12-multiple-response-types--error-bodies)
13. [Auto-Collection with `utoipa-actix-web`](#13-auto-collection-with-utoipa-actix-web)
14. [Feature Flags Reference](#14-feature-flags-reference)
15. [Common Errors & Fixes](#15-common-errors--fixes)

---

## 1. What You're Setting Up

```
Your actix-web handlers
        │
        ▼ #[utoipa::path(...)] annotations
        │
   [utoipa crate] ──► generates /api-docs/openapi.json at compile time
        │
        ▼
[utoipa-swagger-ui] ──► serves interactive UI at /swagger-ui/
```

- **utoipa** — reads your code annotations and produces an OpenAPI 3.0 spec
- **utoipa-swagger-ui** — serves the Swagger UI web interface pointing at that spec
- Everything is **compile-time checked** — docs stay in sync with your actual code

---

## 2. Cargo.toml — Dependencies

```toml
[dependencies]
actix-web    = "4"
serde        = { version = "1", features = ["derive"] }
serde_json   = "1"

# Core utoipa — OpenAPI spec generation
utoipa       = { version = "4", features = ["actix_extras"] }

# Swagger UI server
utoipa-swagger-ui = { version = "7", features = ["actix-web"] }

# Optional: auto-collect routes without listing them manually
utoipa-actix-web = "0.1"
```

> **`actix_extras` feature** lets utoipa automatically parse path params and query params
> from actix-web's `#[get("/path/{id}")]` macros — less boilerplate.

> **`vendored` feature** on `utoipa-swagger-ui` bundles Swagger UI assets into your binary
> (no internet required at runtime):
> ```toml
> utoipa-swagger-ui = { version = "7", features = ["actix-web", "vendored"] }
> ```

---

## 3. Project Structure

```
src/
├── main.rs          ← HttpServer, App, Swagger UI mount, OpenApi derive
├── models.rs        ← Structs with #[derive(ToSchema)]
├── handlers/
│   ├── mod.rs
│   ├── users.rs     ← Route handlers with #[utoipa::path(...)]
│   └── products.rs
└── errors.rs        ← Error types with #[derive(ToSchema)]
```

---

## 4. Step 1 — Define Your Schemas with `ToSchema`

Add `ToSchema` to any struct used in request bodies or responses.
Rust doc comments (`///`) become field descriptions in the UI.

```rust
// src/models.rs
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// A user in the system
#[derive(Serialize, Deserialize, ToSchema)]
pub struct User {
    /// Unique user ID
    pub id: u64,
    /// Full display name
    pub name: String,
    /// Email address (must be unique)
    pub email: String,
    /// Optional age in years
    pub age: Option<u32>,
}

/// Payload to create a new user
#[derive(Serialize, Deserialize, ToSchema)]
pub struct CreateUserRequest {
    /// Full display name
    pub name: String,
    /// Email address
    pub email: String,
    pub age: Option<u32>,
}

/// Generic API error response
#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    /// HTTP status code
    pub status: u16,
    /// Human-readable error message
    pub message: String,
}
```

---

## 5. Step 2 — Annotate Your Route Handlers

Use `#[utoipa::path(...)]` above each handler. The doc comment (`///`) on the function
becomes the endpoint description in Swagger UI.

### GET — list all

```rust
use actix_web::{get, HttpResponse, Responder};
use utoipa;
use crate::models::{User, ErrorResponse};

/// List all users
///
/// Returns every user currently in the system.
#[utoipa::path(
    get,
    path = "/users",
    tag = "Users",
    responses(
        (status = 200, description = "List of users", body = Vec<User>),
        (status = 500, description = "Internal server error", body = ErrorResponse),
    )
)]
#[get("/users")]
pub async fn list_users() -> impl Responder {
    let users: Vec<User> = vec![]; // your DB call here
    HttpResponse::Ok().json(users)
}
```

### GET — single item by path param

```rust
use actix_web::{get, web, HttpResponse, Responder};

/// Get a user by ID
#[utoipa::path(
    get,
    path = "/users/{id}",
    tag = "Users",
    params(
        ("id" = u64, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User found", body = User),
        (status = 404, description = "User not found", body = ErrorResponse),
    )
)]
#[get("/users/{id}")]
pub async fn get_user(id: web::Path<u64>) -> impl Responder {
    // your logic here
    HttpResponse::Ok().json(User {
        id: *id,
        name: "Alice".into(),
        email: "alice@example.com".into(),
        age: Some(30),
    })
}
```

> **Tip:** With `actix_extras` enabled you can omit the `params(...)` block entirely —
> utoipa reads types directly from the function signature.

### POST — create with request body

```rust
use actix_web::{post, web, HttpResponse, Responder};
use crate::models::{CreateUserRequest, User};

/// Create a new user
#[utoipa::path(
    post,
    path = "/users",
    tag = "Users",
    request_body = CreateUserRequest,
    responses(
        (status = 201, description = "User created successfully", body = User),
        (status = 400, description = "Invalid input", body = ErrorResponse),
        (status = 409, description = "Email already in use", body = ErrorResponse),
    )
)]
#[post("/users")]
pub async fn create_user(body: web::Json<CreateUserRequest>) -> impl Responder {
    // your logic here
    HttpResponse::Created().json(User {
        id: 1,
        name: body.name.clone(),
        email: body.email.clone(),
        age: body.age,
    })
}
```

### PUT — update

```rust
use actix_web::{put, web, HttpResponse, Responder};

/// Update an existing user
#[utoipa::path(
    put,
    path = "/users/{id}",
    tag = "Users",
    params(
        ("id" = u64, Path, description = "User ID to update")
    ),
    request_body = CreateUserRequest,
    responses(
        (status = 200, description = "User updated", body = User),
        (status = 404, description = "User not found", body = ErrorResponse),
    )
)]
#[put("/users/{id}")]
pub async fn update_user(
    id: web::Path<u64>,
    body: web::Json<CreateUserRequest>,
) -> impl Responder {
    HttpResponse::Ok().json(User {
        id: *id,
        name: body.name.clone(),
        email: body.email.clone(),
        age: body.age,
    })
}
```

### DELETE

```rust
use actix_web::{delete, web, HttpResponse, Responder};

/// Delete a user
#[utoipa::path(
    delete,
    path = "/users/{id}",
    tag = "Users",
    params(
        ("id" = u64, Path, description = "User ID to delete")
    ),
    responses(
        (status = 204, description = "User deleted"),
        (status = 404, description = "User not found", body = ErrorResponse),
    )
)]
#[delete("/users/{id}")]
pub async fn delete_user(id: web::Path<u64>) -> impl Responder {
    HttpResponse::NoContent().finish()
}
```

---

## 6. Step 3 — Create the OpenAPI Document

Define one central `ApiDoc` struct that lists all your paths and schemas.

```rust
// src/main.rs (or src/api_doc.rs)
use utoipa::OpenApi;
use crate::models::{User, CreateUserRequest, ErrorResponse};
use crate::handlers::users::{list_users, get_user, create_user, update_user, delete_user};

#[derive(OpenApi)]
#[openapi(
    // List every handler function here
    paths(
        list_users,
        get_user,
        create_user,
        update_user,
        delete_user,
    ),
    // List every schema used in requests/responses
    components(
        schemas(User, CreateUserRequest, ErrorResponse)
    ),
    // Define tag descriptions shown in the UI sidebar
    tags(
        (name = "Users", description = "User management endpoints"),
    ),
    info(
        title = "My API",
        version = "1.0.0",
        description = "REST API built with actix-web and documented with utoipa",
        contact(name = "Your Name", email = "you@example.com"),
        license(name = "MIT"),
    ),
)]
pub struct ApiDoc;
```

---

## 7. Step 4 — Mount Swagger UI in actix-web

```rust
// src/main.rs
use actix_web::{web, App, HttpServer};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

mod models;
mod handlers;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            // Your normal API routes
            .service(handlers::users::list_users)
            .service(handlers::users::get_user)
            .service(handlers::users::create_user)
            .service(handlers::users::update_user)
            .service(handlers::users::delete_user)

            // Mount Swagger UI — this is all you need!
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", ApiDoc::openapi()),
            )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

Now visit **http://localhost:8080/swagger-ui/** in your browser. Done. ✅

---

## 8. Full Working Example — CRUD API

A minimal but complete single-file example you can paste and run:

```rust
use actix_web::{delete, get, post, put, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use utoipa::{OpenApi, ToSchema};
use utoipa_swagger_ui::SwaggerUi;

// ── Models ────────────────────────────────────────────────────────────────────

#[derive(Serialize, Deserialize, ToSchema, Clone)]
pub struct Todo {
    pub id: u64,
    pub title: String,
    pub done: bool,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct CreateTodo {
    pub title: String,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ApiError {
    pub message: String,
}

// ── Handlers ──────────────────────────────────────────────────────────────────

/// List all todos
#[utoipa::path(get, path = "/todos", tag = "Todos",
    responses((status = 200, body = Vec<Todo>)))]
#[get("/todos")]
async fn list_todos() -> impl Responder {
    HttpResponse::Ok().json(vec![
        Todo { id: 1, title: "Buy milk".into(), done: false },
    ])
}

/// Get a single todo
#[utoipa::path(get, path = "/todos/{id}", tag = "Todos",
    params(("id" = u64, Path, description = "Todo ID")),
    responses(
        (status = 200, body = Todo),
        (status = 404, body = ApiError),
    ))]
#[get("/todos/{id}")]
async fn get_todo(id: web::Path<u64>) -> impl Responder {
    HttpResponse::Ok().json(Todo { id: *id, title: "Buy milk".into(), done: false })
}

/// Create a todo
#[utoipa::path(post, path = "/todos", tag = "Todos",
    request_body = CreateTodo,
    responses((status = 201, body = Todo)))]
#[post("/todos")]
async fn create_todo(body: web::Json<CreateTodo>) -> impl Responder {
    HttpResponse::Created().json(Todo { id: 42, title: body.title.clone(), done: false })
}

/// Delete a todo
#[utoipa::path(delete, path = "/todos/{id}", tag = "Todos",
    params(("id" = u64, Path, description = "Todo ID")),
    responses((status = 204, description = "Deleted")))]
#[delete("/todos/{id}")]
async fn delete_todo(id: web::Path<u64>) -> impl Responder {
    HttpResponse::NoContent().finish()
}

// ── OpenAPI Doc ───────────────────────────────────────────────────────────────

#[derive(OpenApi)]
#[openapi(
    paths(list_todos, get_todo, create_todo, delete_todo),
    components(schemas(Todo, CreateTodo, ApiError)),
    tags((name = "Todos", description = "Todo management")),
    info(title = "Todo API", version = "1.0.0"),
)]
struct ApiDoc;

// ── Server ────────────────────────────────────────────────────────────────────

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(list_todos)
            .service(get_todo)
            .service(create_todo)
            .service(delete_todo)
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", ApiDoc::openapi()),
            )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

---

## 9. Query Parameters with `IntoParams`

Use `IntoParams` on a struct to document query string parameters (`?page=1&limit=20`).

```rust
use utoipa::IntoParams;
use serde::Deserialize;

/// Pagination query parameters
#[derive(Deserialize, IntoParams)]
pub struct PaginationParams {
    /// Page number (default: 1)
    #[param(minimum = 1, default = 1)]
    pub page: Option<u32>,

    /// Results per page (default: 20, max: 100)
    #[param(minimum = 1, maximum = 100, default = 20)]
    pub limit: Option<u32>,
}

/// Search filters
#[derive(Deserialize, IntoParams)]
pub struct SearchParams {
    /// Search query string
    pub q: Option<String>,
}
```

Reference them in the handler:

```rust
/// List users with pagination
#[utoipa::path(
    get,
    path = "/users",
    tag = "Users",
    params(PaginationParams, SearchParams),
    responses(
        (status = 200, description = "Paginated user list", body = Vec<User>)
    )
)]
#[get("/users")]
pub async fn list_users(
    query: web::Query<PaginationParams>,
    search: web::Query<SearchParams>,
) -> impl Responder {
    HttpResponse::Ok().json(vec![] as Vec<User>)
}
```

---

## 10. JWT Bearer Auth in Swagger UI

Add a JWT security scheme so the "Authorize 🔒" button appears in Swagger UI.

### Step A — Create a `SecurityAddon`

```rust
// src/main.rs
use utoipa::{
    openapi::security::{HttpAuthScheme, HttpBuilder, SecurityScheme},
    Modify, OpenApi,
};

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
```

### Step B — Register it in `OpenApi`

```rust
#[derive(OpenApi)]
#[openapi(
    paths(...),
    components(schemas(...)),
    modifiers(&SecurityAddon),   // ← add this line
)]
pub struct ApiDoc;
```

### Step C — Mark protected endpoints with `security`

```rust
/// Get current user profile (requires auth)
#[utoipa::path(
    get,
    path = "/me",
    tag = "Auth",
    security(("bearer_auth" = [])),   // ← locks this endpoint in UI
    responses(
        (status = 200, body = User),
        (status = 401, description = "Unauthorized", body = ErrorResponse),
    )
)]
#[get("/me")]
pub async fn get_me() -> impl Responder {
    HttpResponse::Ok().json(User {
        id: 1,
        name: "Alice".into(),
        email: "alice@example.com".into(),
        age: Some(30),
    })
}
```

Now in Swagger UI you'll see a lock icon on protected endpoints and a global
"Authorize" button where you can paste a JWT to test authenticated routes.

---

## 11. API Tags and Grouping

Tags group your endpoints in the Swagger UI sidebar. Define them at the `OpenApi` level:

```rust
#[derive(OpenApi)]
#[openapi(
    paths(...),
    components(schemas(...)),
    tags(
        (name = "Auth",     description = "Login, register, tokens"),
        (name = "Users",    description = "User profile management"),
        (name = "Products", description = "Product catalog operations"),
        (name = "Orders",   description = "Order placement and tracking"),
    ),
)]
pub struct ApiDoc;
```

Then on each handler use `tag = "Users"` (or whichever tag applies) in `#[utoipa::path(...)]`.

---

## 12. Multiple Response Types & Error Bodies

Document different response shapes per status code:

```rust
/// Create a product
#[utoipa::path(
    post,
    path = "/products",
    tag = "Products",
    request_body = CreateProductRequest,
    responses(
        (status = 201, description = "Product created",        body = Product),
        (status = 400, description = "Validation failed",      body = ErrorResponse),
        (status = 401, description = "Unauthorized",           body = ErrorResponse),
        (status = 409, description = "Product already exists", body = ErrorResponse),
        (status = 500, description = "Internal server error",  body = ErrorResponse),
    ),
    security(("bearer_auth" = []))
)]
#[post("/products")]
pub async fn create_product(body: web::Json<CreateProductRequest>) -> impl Responder {
    HttpResponse::Created().finish()
}
```

You can also add inline response examples:

```rust
responses(
    (
        status = 200,
        description = "User found",
        body = User,
        example = json!({
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30
        })
    ),
)
```

---

## 13. Auto-Collection with `utoipa-actix-web`

With `utoipa-actix-web`, you no longer need to list every handler in `#[openapi(paths(...))]`.
Routes are collected **automatically** from your `.service(...)` calls.

```toml
# Cargo.toml
utoipa-actix-web = "0.1"
```

```rust
use utoipa_actix_web::{scope, AppExt};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        let (app, api) = App::new()
            .into_utoipa_app()                         // ← wraps App
            .service(
                scope("/api/v1")
                    .service(handlers::users::list_users)
                    .service(handlers::users::get_user)
                    .service(handlers::users::create_user)
            )
            .split_for_parts();                        // ← extracts collected OpenAPI spec

        app.service(
            SwaggerUi::new("/swagger-ui/{_:.*}")
                .url("/api-docs/openapi.json", api),
        )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

> ⚠️ Only `.service(handler)` calls are auto-collected. Manual `.route(...)` registrations
> are not supported — use the standard `#[openapi(paths(...))]` approach for those.

---

## 14. Feature Flags Reference

### utoipa features

| Feature         | What it enables                                              |
|-----------------|--------------------------------------------------------------|
| `actix_extras`  | Auto-parse path/query params from actix macros (recommended) |
| `chrono`        | `DateTime`, `NaiveDate`, `Duration` type support             |
| `uuid`          | `Uuid` type support                                          |
| `decimal`       | `rust_decimal::Decimal` type support                         |
| `yaml`          | Serialize OpenAPI spec to YAML format                        |
| `debug`         | Adds `Debug` trait to OpenAPI types                          |
| `non_strict_integers` | Extra int formats: `int8`, `int16`, `uint8`, `uint16`  |
| `rc_schema`     | `ToSchema` for `Arc<T>` and `Rc<T>`                          |

### utoipa-swagger-ui features

| Feature         | What it enables                                              |
|-----------------|--------------------------------------------------------------|
| `actix-web`     | actix-web integration (required for this setup)              |
| `vendored`      | Bundle Swagger UI assets into binary (offline use)           |
| `reqwest`       | Use reqwest to download Swagger UI (cross-platform builds)   |
| `debug-embed`   | Embed assets in debug builds too                             |
| `cache`         | Cache Swagger UI download during builds                      |

---

## 15. Common Errors & Fixes

### ❌ `the trait ToSchema is not implemented for SomeType`

Add `#[derive(ToSchema)]` to that struct, and add it to `components(schemas(...))` in your `OpenApi` derive.

---

### ❌ `schemas and paths not showing in Swagger UI`

Make sure every handler listed in `paths(...)` has the `#[utoipa::path(...)]` macro,
and every schema used is listed in `components(schemas(...))`.

---

### ❌ Path params not appearing

Either add them manually:
```rust
params(("id" = u64, Path, description = "The user ID"))
```
Or enable `actix_extras` in Cargo.toml:
```toml
utoipa = { version = "4", features = ["actix_extras"] }
```

---

### ❌ Swagger UI shows but spec is empty

You forgot to list your handlers in `#[openapi(paths(...))]`. Each handler must appear there.

---

### ❌ `SwaggerUi::new` — 404 on `/swagger-ui/`

Make sure the path pattern ends with `{_:.*}`:
```rust
SwaggerUi::new("/swagger-ui/{_:.*}")
//                             ^^^^ required
```

---

### ❌ Build fails downloading Swagger UI assets

Use the `vendored` feature to avoid the network download at build time:
```toml
utoipa-swagger-ui = { version = "7", features = ["actix-web", "vendored"] }
```

---

## Quick Reference — `#[utoipa::path(...)]` Attributes

```rust
#[utoipa::path(
    METHOD,                           // get | post | put | patch | delete
    path = "/route/{param}",          // URL path
    tag = "GroupName",                // Swagger UI sidebar group
    operation_id = "unique_op_name",  // optional unique name

    params(
        ("param" = Type, Path,  description = "..."),   // path param
        ("q"     = Type, Query, description = "..."),   // query param
        ("X-Key" = Type, Header, description = "..."),  // header param
        StructWithIntoParams,                           // whole struct
    ),

    request_body = MyRequestStruct,   // POST/PUT body schema

    request_body(
        content = MyRequestStruct,
        description = "The request payload",
        content_type = "application/json"
    ),

    responses(
        (status = 200, description = "Success",  body = ResponseStruct),
        (status = 204, description = "No content"),
        (status = 400, description = "Bad request", body = ErrorResponse),
    ),

    security(
        ("bearer_auth" = []),          // requires JWT auth
        ("api_key" = []),              // requires API key
    ),
)]
```

---

## URLs After Setup

| URL | What you get |
|-----|-------------|
| `http://localhost:8080/swagger-ui/` | Interactive Swagger UI |
| `http://localhost:8080/api-docs/openapi.json` | Raw OpenAPI JSON spec |

You can also feed the JSON to **Postman**, **Insomnia**, **Scalar**, or **Redoc** for alternative views.

---

*Generated for utoipa v4 + utoipa-swagger-ui v7 + actix-web v4 — June 2026*
