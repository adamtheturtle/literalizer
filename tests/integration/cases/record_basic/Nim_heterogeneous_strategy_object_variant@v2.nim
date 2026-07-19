import tables
type
  ValueKind = enum
    vkInt, vkStr, vkBool, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkBool: boolVal: bool
    of vkList: listVal: seq[Value]
var my_data = {
    "id": Value(kind: vkInt, intVal: 1),
    "description": Value(kind: vkStr, strVal: "She said \"hello\", then waved"),
    "is_done": Value(kind: vkBool, boolVal: false),
    "blocks": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1), Value(kind: vkInt, intVal: 2), Value(kind: vkInt, intVal: 3)])
}.toTable
