struct FooType2; bar; end
struct FooType1; Foo; end
struct AType; foo; end
a = AType(FooType1(FooType2((args...; kwargs...) -> nothing)))
a.foo.Foo.bar(x=[1])
