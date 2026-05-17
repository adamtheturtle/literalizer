{.warning[UnusedImport]:off.}
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
