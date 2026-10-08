type HelperType = object
template list(self: HelperType; args: varargs[untyped]) = discard
var helper: HelperType
helper.list(1)
