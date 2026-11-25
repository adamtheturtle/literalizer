class FooType; def bar(*a, **kw); end; end
class FooType; def Foo; FooType.new; end; end
class AType; def foo; FooType.new; end; end
a = AType.new
my_data = a.foo.Foo.bar(x: [1])
