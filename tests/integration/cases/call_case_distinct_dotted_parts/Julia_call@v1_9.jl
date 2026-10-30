struct FooType; bar; end
struct FooType; Foo; end
struct AType; foo; end
a = AType(FooType(FooType((args...; kwargs...) -> nothing)))
a.foo.Foo.bar(x=[1])
