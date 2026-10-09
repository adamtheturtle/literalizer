struct ThingType; go; end
struct OuterType; thing; end
outer = OuterType(ThingType((args...; kwargs...) -> nothing))
outer.thing.go()
