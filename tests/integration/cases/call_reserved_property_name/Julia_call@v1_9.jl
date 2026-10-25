struct FooType; class; end
foo = FooType((args...; kwargs...) -> nothing)
foo.class(value=1)
