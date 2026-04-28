type ClientType_ = object
type ApiType_ = object
    client: ClientType_
type ObjType_ = object
    api: ApiType_
proc post(self: ClientType_; _args: varargs[untyped]) = discard
var obj: ObjType_
obj.api.client.post("hello")
obj.api.client.post(42)
obj.api.client.post(true)
