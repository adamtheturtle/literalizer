type FooType = object
template class(self: FooType; args: varargs[untyped]) = discard
var foo: FooType
foo.class(1)
