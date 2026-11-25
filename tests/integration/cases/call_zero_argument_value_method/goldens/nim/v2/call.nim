type ThingType = object
proc go(self: ThingType): int {.discardable.} = 0
var thing: ThingType
thing.go()
