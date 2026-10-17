{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
type ClientType = object
type AppType = object
    client: ClientType
template go(self: ClientType; args: varargs[untyped]) = discard
var app: AppType
app.client.go(@[Value(kind: vkInt, intVal: 1)], @[Value(kind: vkStr, strVal: "text")])
