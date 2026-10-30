class _FooType2 { def bar(Map _args) { null } }
class _FooType1 { def Foo = new _FooType2() }
class _AType { def foo = new _FooType1() }
def a = new _AType()
def my_data = a.foo.Foo.bar(x: [1])
