type FooType2 = object
type FooType1 = object
    Foo: FooType2
type AType = object
    foo: FooType1
template bar(self: FooType2; args: varargs[untyped]) = discard
var a: AType
a.foo.Foo.bar([1])
