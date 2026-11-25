{.warning[UnusedImport]:off.}
import tables
type AppType = object
template go(self: AppType; args: varargs[untyped]) = discard
var app: AppType
app.go(@[1], @["text"])
