type ClientType_ = object
type AppType_ = object
    client: ClientType_
proc fetch(self: ClientType_; _args: varargs[untyped]): untyped = 0
var app: AppType_
proc emit(_args: varargs[untyped]) = discard
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
