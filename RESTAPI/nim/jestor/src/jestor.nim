import jester, asyncdispatch

settings:
  port = Port(5000)

routes:
  get "/hello":
    resp "hello"

when isMainModule:
  runForever()

