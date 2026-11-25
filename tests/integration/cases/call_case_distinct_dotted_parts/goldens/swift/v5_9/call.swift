class _FooType { @discardableResult func bar(x: Any = 0) -> Any { 0 } }
class _fooType { var Foo = _FooType() }
class _aType { var foo = _fooType() }
let a = _aType()
a.foo.Foo.bar(x: [1]);
