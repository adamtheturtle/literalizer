class _FooType { def bar(Map _args) { null } }
class _FooType { def Foo = new _FooType() }
class _AType { def foo = new _FooType() }
def a = new _AType()
a.foo.Foo.bar(x: [1])
