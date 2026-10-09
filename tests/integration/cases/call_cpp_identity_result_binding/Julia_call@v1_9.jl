struct ThingType; go; end
thing = ThingType((args...; kwargs...) -> nothing)
my_data = thing.go(value=[])
