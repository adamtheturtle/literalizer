type ThingType = object
proc go[T0](self: ThingType; value: T0): int {.discardable.} = 0
var thing: ThingType
var item = @[
    1,
    2
]
thing.go(item)
