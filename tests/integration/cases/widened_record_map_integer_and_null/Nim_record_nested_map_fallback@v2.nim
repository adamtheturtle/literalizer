{.warning[UnusedImport]:off.}
import tables
type
  ValueKind = enum
    vkInt, vkNull
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkNull: discard
type Record0 = object
    input: Table[string, Value]
var my_data = @[
    Record0(input: {"a": Value(kind: vkInt, intVal: 1)}.toTable),
    Record0(input: {"b": Value(kind: vkNull)}.toTable)
]
