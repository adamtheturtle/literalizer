struct FoobarType; bar; end
struct Foo_barType; fooBar; end
struct AType; foo_bar; end
a = AType(Foo_barType(FoobarType((args...; kwargs...) -> nothing)))
a.foo_bar.fooBar.bar(x=[1])
