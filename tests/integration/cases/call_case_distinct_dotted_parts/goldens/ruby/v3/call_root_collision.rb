class FooType; def bar(*a, **kw); end; end
class FooType; def Foo; FooType.new; end; end
foo = FooType.new
foo.Foo.bar(x: [1])
