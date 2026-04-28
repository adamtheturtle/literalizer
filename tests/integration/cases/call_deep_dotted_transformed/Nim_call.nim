type ClientType = object
type AppType = object
    client: ClientType
proc fetch(self: ClientType; args: varargs[untyped]): untyped = 0
var app: AppType
proc emit(args: varargs[untyped]) = discard
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
