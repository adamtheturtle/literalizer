type ObjType = object
template class(self: ObjType; args: varargs[untyped]) = discard
var obj: ObjType
obj.class(42)
