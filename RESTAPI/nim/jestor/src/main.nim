# main.nim
# Entry point — Simple HTTP server using pure Nim async

import std/[asyncnet, asyncdispatch, json, strutils, os]

# ── Settings ───────────────────────────────────────────────────
const
  HOST = "0.0.0.0"
  APP_PORT = 5000

# ── Response Models ─────────────────────────────────────────────
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

# ── Request Parsing ───────────────────────────────────────────
proc parseRequest(body: string): string =
  try:
    let parsed = parseJson(body)
    if parsed.hasKey("name"):
      result = parsed["name"].getStr()
    else:
      result = ""
  except:
    result = ""

# ── Route Handler ─────────────────────────────────────────────
proc handleRequest(path: string, body: string, httpMethod: string): string =
  case path
  of "/":
    return """{"message": "API is running", "status": 200}"""
  of "/hello":
    if httpMethod == "GET":
      let response = newHelloResponse(message = "hello")
      return responseToJson(response)
    elif httpMethod == "POST":
      let name = parseRequest(body)
      if name.len > 0:
        let response = newHelloResponse(message = "hello, " & name & "!")
        return responseToJson(response)
      else:
        let response = newHelloResponse(message = "hello")
        return responseToJson(response)
    else:
      let response = newHelloResponse(message = "Method not allowed", status = 405, success = false)
      return responseToJson(response)
  else:
    let response = newHelloResponse(message = "Not found", status = 404, success = false)
    return responseToJson(response)

# ── HTTP Response Builder ──────────────────────────────────────
proc buildResponse(body: string, statusCode: int = 200, contentType: string = "application/json"): string =
  let statusText = case statusCode
    of 200: "OK"
    of 400: "Bad Request"
    of 404: "Not Found"
    of 405: "Method Not Allowed"
    else: "OK"

  return "HTTP/1.1 " & $statusCode & " " & statusText & "\c\L" &
         "Content-Type: " & contentType & "\c\L" &
         "Content-Length: " & $body.len & "\c\L\c\L" &
         body

# ── Request Handler ───────────────────────────────────────────
proc handleClient(client: AsyncSocket) {.async.} =
  try:
    while true:
      let data = await client.recvLine()
      if data.len == 0:
        break

      # Parse HTTP request line
      let parts = data.split(" ")
      if parts.len < 2:
        continue

      let httpMethod = parts[0]
      let path = parts[1]

      # Read headers
      var contentLength = 0
      while true:
        let headerLine = await client.recvLine()
        if headerLine.len == 0:
          break
        if headerLine.toLowerAscii.startsWith("content-length:"):
          contentLength = parseInt(headerLine.split(":")[1].strip())

      # Read body if present
      var body = ""
      if contentLength > 0:
        body = await client.recv(contentLength)

      # Handle request
      let responseBody = handleRequest(path, body, httpMethod)
      let httpResponse = buildResponse(responseBody)

      await client.send(httpResponse)

  except Exception as e:
    echo "Error handling client: ", e.msg
  finally:
    client.close()

# ── Main Server ───────────────────────────────────────────────
proc main() {.async.} =
  let socket = newAsyncSocket()
  socket.setSockOpt(OptReuseAddr, true)
  socket.bindAddr(Port(APP_PORT), HOST)
  socket.listen()

  echo "🚀 Server starting on http://", HOST, ":", APP_PORT
  echo "📍 Routes:"
  echo "   GET  /        --> health check"
  echo "   GET  /hello   --> returns hello"
  echo "   POST /hello   --> greets by name"
  echo ""

  while true:
    let client = await socket.accept()
    asyncCheck handleClient(client)

# ── Start ─────────────────────────────────────────────────────
waitFor main()
