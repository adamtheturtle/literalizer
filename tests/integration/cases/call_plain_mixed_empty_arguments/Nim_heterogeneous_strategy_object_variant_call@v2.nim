{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
proc make_widget[T0, T1, T2](before: T0; populated: T1; after: T2): int {.discardable.} = 0
proc make_widget[T1](before: array[0, int]; populated: T1; after: array[0, int]): int {.discardable.} = 0
proc make_widget[T0, T1](before: T0; populated: T1; after: array[0, int]): int {.discardable.} = 0
make_widget(newSeq[string](), @[Value(kind: vkInt, intVal: 1)], newSeq[string]())
make_widget(@[Value(kind: vkStr, strVal: "text")], @[Value(kind: vkInt, intVal: 2)], newSeq[string]())
make_widget(newSeq[string](), @[Value(kind: vkStr, strVal: "text")], newSeq[string]())
make_widget(@[Value(kind: vkStr, strVal: "text")], @[Value(kind: vkInt, intVal: 2)], @[Value(kind: vkInt, intVal: 3)])
