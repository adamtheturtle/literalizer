type ClientType = object
type AppType = object
    client: ClientType
template fetch(self: ClientType; args: varargs[untyped]): untyped {.discardable.} = 0
var app: AppType
template emit(args: varargs[untyped]) = discard
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
