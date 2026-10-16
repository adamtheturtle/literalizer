{.warning[UnusedImport]:off.}
import tables
type ThingType = object
proc go[T0, T1, T2](self: ThingType; before: T0; populated: T1; after: T2): int {.discardable.} = 0
proc go[T1](self: ThingType; before: array[0, int]; populated: T1; after: array[0, int]): int {.discardable.} = 0
proc go[T0, T1](self: ThingType; before: T0; populated: T1; after: array[0, int]): int {.discardable.} = 0
var thing: ThingType
thing.go(newSeq[string](), @[1], newSeq[string]())
thing.go(@["text"], @[2], newSeq[string]())
thing.go(newSeq[string](), @["text"], newSeq[string]())
thing.go(@["text"], @[2], @[3])
