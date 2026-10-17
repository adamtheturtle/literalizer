{.warning[UnusedImport]:off.}
import tables
type ClientType = object
type AppType = object
    client: ClientType
template go(self: ClientType; args: varargs[untyped]) = discard
var app: AppType
app.client.go(@[1], @["text"])
