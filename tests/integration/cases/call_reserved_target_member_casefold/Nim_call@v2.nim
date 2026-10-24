type ObjType = object
template BEGIN(self: ObjType; args: varargs[untyped]) = discard
var obj: ObjType
obj.BEGIN(42)
