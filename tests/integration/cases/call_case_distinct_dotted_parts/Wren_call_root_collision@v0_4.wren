class FooFoo_ {
    construct new() {}
    bar(x) {}
}
class Foo_ {
    Foo { _Foo }
    construct new() {
        _Foo = FooFoo_.new()
    }
}
var foo = Foo_.new()
foo.Foo.bar([1])
