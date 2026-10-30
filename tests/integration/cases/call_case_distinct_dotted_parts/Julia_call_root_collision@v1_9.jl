struct FooType; bar; end
struct FooType; Foo; end
foo = FooType(FooType((args...; kwargs...) -> nothing))
foo.Foo.bar(x=[1])
