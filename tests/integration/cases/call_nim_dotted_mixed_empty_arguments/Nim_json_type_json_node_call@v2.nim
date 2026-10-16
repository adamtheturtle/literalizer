{.warning[UnusedImport]:off.}
import json
type ThingType = object
proc go[T0, T1, T2](self: ThingType; before: T0; populated: T1; after: T2): int {.discardable.} = 0
var thing: ThingType
thing.go(newJArray(), %*([1]), newJArray())
thing.go(%*(["text"]), %*([2]), newJArray())
thing.go(newJArray(), %*(["text"]), newJArray())
thing.go(%*(["text"]), %*([2]), %*([3]))
