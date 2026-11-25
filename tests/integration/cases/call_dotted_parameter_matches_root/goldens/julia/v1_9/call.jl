struct OuterType; inner; end
outer = OuterType((args...; kwargs...) -> nothing)
outer.inner(outer=1, n=2)
