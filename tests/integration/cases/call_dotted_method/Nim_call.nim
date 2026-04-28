type ClientType = object
type AppType = object
    client: ClientType
proc fetch(self: ClientType; args: varargs[untyped]) = discard
var app: AppType
app.client.fetch("hello")
app.client.fetch(42)
app.client.fetch(true)
