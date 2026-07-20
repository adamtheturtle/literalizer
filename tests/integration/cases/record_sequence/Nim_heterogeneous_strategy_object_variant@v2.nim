import tables
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
var my_data = @[
    {"id": Value(kind: vkInt, intVal: 1), "label": Value(kind: vkStr, strVal: "first"), "tags": Value(kind: vkList, listVal: newSeq[Value]())}.toTable,
    {"id": Value(kind: vkInt, intVal: 2), "label": Value(kind: vkStr, strVal: "second"), "tags": Value(kind: vkList, listVal: newSeq[Value]())}.toTable,
    {"id": Value(kind: vkInt, intVal: 3), "label": Value(kind: vkStr, strVal: "third"), "tags": Value(kind: vkList, listVal: newSeq[Value]())}.toTable
]
