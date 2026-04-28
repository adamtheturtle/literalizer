type ClientType_ = object
type AppType_ = object
    client: ClientType_
proc fetch(self: ClientType_; _args: varargs[untyped]) = discard
var app: AppType_
app.client.fetch("hello")
app.client.fetch(42)
app.client.fetch(true)
