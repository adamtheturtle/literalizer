class _FoobarType { def bar(Map _args) { null } }
class _Foo_BarType { def fooBar = new _FoobarType() }
class _AType { def foo_bar = new _Foo_BarType() }
def a = new _AType()
a.foo_bar.fooBar.bar(x: [1])
