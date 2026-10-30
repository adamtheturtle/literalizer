class _FooType { def bar(Map _args) { null } }
class _FooType { def Foo = new _FooType() }
def foo = new _FooType()
foo.Foo.bar(x: [1])
