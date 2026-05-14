import tables
type
  ValueKind = enum
    vkInt, vkStr
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = @[
    {"id": Value(kind: vkInt, intVal: 1), "label": Value(kind: vkStr, strVal: "first")}.toTable,
    {"id": Value(kind: vkInt, intVal: 2), "label": Value(kind: vkStr, strVal: "second")}.toTable,
    {"id": Value(kind: vkInt, intVal: 3), "label": Value(kind: vkStr, strVal: "third")}.toTable
]
