class _FooType1 { def bar(Map _args) { null } }
class _FooType0 { def Foo = new _FooType1() }
def foo = new _FooType0()
foo.Foo.bar(x: [1])
