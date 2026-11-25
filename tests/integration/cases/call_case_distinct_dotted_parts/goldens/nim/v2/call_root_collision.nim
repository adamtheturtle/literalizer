type FooType1 = object
type FooType0 = object
    Foo: FooType1
template bar(self: FooType1; args: varargs[untyped]) = discard
var foo: FooType0
foo.Foo.bar([1])
