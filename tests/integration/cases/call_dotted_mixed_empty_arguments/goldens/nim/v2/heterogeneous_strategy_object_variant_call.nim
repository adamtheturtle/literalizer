{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
type ThingType = object
proc go[T0, T1, T2](self: ThingType; before: T0; populated: T1; after: T2): int {.discardable.} = 0
proc go[T1](self: ThingType; before: array[0, int]; populated: T1; after: array[0, int]): int {.discardable.} = 0
proc go[T0, T1](self: ThingType; before: T0; populated: T1; after: array[0, int]): int {.discardable.} = 0
var thing: ThingType
thing.go(newSeq[string](), @[Value(kind: vkInt, intVal: 1)], newSeq[string]())
thing.go(@[Value(kind: vkStr, strVal: "text")], @[Value(kind: vkInt, intVal: 2)], newSeq[string]())
thing.go(newSeq[string](), @[Value(kind: vkStr, strVal: "text")], newSeq[string]())
thing.go(@[Value(kind: vkStr, strVal: "text")], @[Value(kind: vkInt, intVal: 2)], @[Value(kind: vkInt, intVal: 3)])
