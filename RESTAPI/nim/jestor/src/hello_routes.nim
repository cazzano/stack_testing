# hello_routes.nim
# Defines the /hello endpoint and its handler logic

import jester
import std/json

# ── Request Model ──────────────────────────────────────────────
type
  HelloRequest = object
    name: string

# ── Response Model ─────────────────────────────────────────────
type
  HelloResponse = object
    message: string
    status: int
    success: bool

# ── Constructors ───────────────────────────────────────────────
proc newHelloResponse(message: string, status: int = 200, success: bool = true): HelloResponse =
  HelloResponse(
    message: message,
    status: status,
    success: success
  )

# ── JSON Serialization ─────────────────────────────────────────
proc responseToJson(res: HelloResponse): string =
  $ %*{
    "message": res.message,
    "status": res.status,
    "success": res.success
  }

proc requestFromJson(body: string): HelloRequest =
  try:
    let parsed = parseJson(body)
    HelloRequest(
      name: if parsed.hasKey("name"): parsed["name"].getStr() else: ""
    )
  except:
    HelloRequest(name: "")

# ── Handler ────────────────────────────────────────────────────

proc handleHelloGet(): HelloResponse =
  ## GET /hello --> returns plain "hello" message
  newHelloResponse(message = "hello")

proc handleHelloPost(body: string): HelloResponse =
  ## POST /hello --> greets by name if provided in request body
  let request = requestFromJson(body)
  if request.name.len > 0:
    newHelloResponse(message = "hello, " & request.name & "!")
  else:
    newHelloResponse(message = "hello")

# ── Router ─────────────────────────────────────────────────────

router helloRouter:

  # GET /hello
  get "/hello":
    let response = handleHelloGet()
    resp Http200, responseToJson(response), "application/json"

  # POST /hello  (body: { "name": "Ali" })
  post "/hello":
    let response = handleHelloPost(request.body)
    let httpCode = if response.success: Http200 else: Http400
    resp httpCode, responseToJson(response), "application/json"
