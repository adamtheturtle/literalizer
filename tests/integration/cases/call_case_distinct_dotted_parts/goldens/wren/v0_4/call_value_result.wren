class AFooFoo_ {
    construct new() {}
    bar(x) {}
}
class AFoo_ {
    Foo { _Foo }
    construct new() {
        _Foo = AFooFoo_.new()
    }
}
class A_ {
    foo { _foo }
    construct new() {
        _foo = AFoo_.new()
    }
}
var a = A_.new()
var my_data = a.foo.Foo.bar([1])
