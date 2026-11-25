type ThingType = object
type OuterType = object
    thing: ThingType
proc go(self: ThingType): int {.discardable.} = 0
var outer: OuterType
outer.thing.go()
