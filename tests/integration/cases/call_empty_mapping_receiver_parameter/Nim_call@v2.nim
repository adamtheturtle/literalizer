type ApiType = object
template process(self: ApiType; args: varargs[untyped]) = discard
var api: ApiType
api.process({})
