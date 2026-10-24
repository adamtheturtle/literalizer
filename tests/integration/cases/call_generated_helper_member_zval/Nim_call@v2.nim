type ObjType = object
template ZVal(self: ObjType; args: varargs[untyped]) = discard
var obj: ObjType
obj.ZVal(1)
