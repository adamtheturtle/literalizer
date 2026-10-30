type FoobarType2 = object
type Foo_BarType1 = object
    fooBar: FoobarType2
type AType = object
    foo_bar: Foo_BarType1
template bar(self: FoobarType2; args: varargs[untyped]) = discard
var a: AType
a.foo_bar.fooBar.bar([1])
