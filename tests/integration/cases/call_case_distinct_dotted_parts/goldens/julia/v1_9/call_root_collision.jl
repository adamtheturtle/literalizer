struct FooType1; bar; end
struct FooType0; Foo; end
foo = FooType0(FooType1((args...; kwargs...) -> nothing))
foo.Foo.bar(x=[1])
