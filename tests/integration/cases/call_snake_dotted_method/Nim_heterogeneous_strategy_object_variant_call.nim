{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkStr, vkInt, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
type Http_ClientType = object
type My_AppType = object
    http_client: Http_ClientType
template fetch(self: Http_ClientType; args: varargs[untyped]) = discard
var my_app: My_AppType
my_app.http_client.fetch("hello")
my_app.http_client.fetch(42)
my_app.http_client.fetch(true)
