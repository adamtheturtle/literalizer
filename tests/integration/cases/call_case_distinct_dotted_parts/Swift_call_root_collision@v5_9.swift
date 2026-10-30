class _FooType { @discardableResult func bar(x: Any = 0) -> Any { 0 } }
class _fooType { var Foo = _FooType() }
let foo = _fooType()
foo.Foo.bar(x: [1]);
