type FooType2 = object
type FooType1 = object
    Foo: FooType2
type AType = object
    foo: FooType1
proc bar[T0](self: FooType2; x: T0): int {.discardable.} = 0
var a: AType
var my_data = a.foo.Foo.bar([1])
