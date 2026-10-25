type ObjType = object
template ZKV(self: ObjType; args: varargs[untyped]) = discard
var obj: ObjType
obj.ZKV(1)
