type ClassType = object
template member(self: ClassType; args: varargs[untyped]) = discard
var class: ClassType
class.member(42)
