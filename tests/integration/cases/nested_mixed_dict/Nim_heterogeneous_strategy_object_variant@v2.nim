import tables
type
  ValueKind = enum
    vkInt, vkStr, vkNull
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkNull: discard
var my_data = {
    "outer": {"a": Value(kind: vkInt, intVal: 1), "b": Value(kind: vkStr, strVal: "x"), "c": Value(kind: vkNull)}.toTable
}.toTable
