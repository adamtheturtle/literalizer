struct ThingType; go; end
thing = ThingType((args...; kwargs...) -> nothing)
thing.go(before=[], populated=[1], after=[])
thing.go(before=["text"], populated=[2], after=[])
thing.go(before=[], populated=["text"], after=[])
thing.go(before=["text"], populated=[2], after=[3])
