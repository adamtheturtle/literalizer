type OuterType = object
template inner(self: OuterType; args: varargs[untyped]) = discard
var outer: OuterType
outer.inner(1, 2)
