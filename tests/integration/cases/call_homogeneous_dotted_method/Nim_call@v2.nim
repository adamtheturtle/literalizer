type ClientType = object
type AppType = object
    client: ClientType
template fetch(self: ClientType; args: varargs[untyped]) = discard
var app: AppType
app.client.fetch("hello")
app.client.fetch("world")
