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
type ApiType = object
    client: ClientType
type ObjType = object
    api: ApiType
template post(self: ClientType; args: varargs[untyped]) = discard
var obj: ObjType
obj.api.client.post("hello")
obj.api.client.post(42)
obj.api.client.post(true)
