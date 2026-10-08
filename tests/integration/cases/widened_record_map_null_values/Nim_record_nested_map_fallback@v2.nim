{.warning[UnusedImport]:off.}
import tables
type
  ValueKind = enum
    vkNull
  Value = object
    case kind: ValueKind
    of vkNull: discard
type Record0 = object
    input: Table[string, Value]
var my_data = @[
    Record0(input: {"a": Value(kind: vkNull)}.toTable),
    Record0(input: {"b": Value(kind: vkNull)}.toTable)
]
