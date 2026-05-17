{.warning[UnusedImport]:off.}
type ClientType = object
type AppType = object
    client: ClientType
proc fetch[T0](self: ClientType; payload: T0): int {.discardable.} = 0
var app: AppType
template emit(args: varargs[untyped]) = discard
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
