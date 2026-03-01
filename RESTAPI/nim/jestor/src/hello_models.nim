# hello_models.nim
# Request and Response models for the Hello API

import json

# ── Request Model ──────────────────────────────────────────────
type
  HelloRequest* = object
    name*: string  # optional name to greet (can be empty)

# ── Response Model ─────────────────────────────────────────────
type
  HelloResponse* = object
    message*: string
    status*:  int
    success*: bool

# ── Constructors ───────────────────────────────────────────────
proc newHelloResponse*(message: string, status: int = 200, success: bool = true): HelloResponse =
  HelloResponse(
    message: message,
    status:  status,
    success: success
  )

# ── JSON Serialization ─────────────────────────────────────────
proc toHelloJson*(res: HelloResponse): JsonNode =
  %*{
    "message": res.message,
    "status":  res.status,
    "success": res.success
  }

proc toHelloJson*(req: HelloRequest): JsonNode =
  %*{
    "name": req.name
  }

# ── JSON Deserialization ───────────────────────────────────────
proc fromHelloJson*(body: JsonNode): HelloRequest =
  HelloRequest(
    name: if body.hasKey("name"): body["name"].getStr() else: ""
  )
