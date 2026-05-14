{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkStr, vkInt, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
type ClientType = object
type AppType = object
    client: ClientType
template fetch(self: ClientType; args: varargs[untyped]) = discard
var app: AppType
app.client.fetch("hello")
app.client.fetch(42)
app.client.fetch(true)
