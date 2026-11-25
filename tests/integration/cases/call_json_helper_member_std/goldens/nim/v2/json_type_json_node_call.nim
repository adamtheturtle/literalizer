{.warning[UnusedImport]:off.}
import json
type ObjType = object
template std(self: ObjType; args: varargs[untyped]) = discard
var obj: ObjType
obj.std(%*(1))
