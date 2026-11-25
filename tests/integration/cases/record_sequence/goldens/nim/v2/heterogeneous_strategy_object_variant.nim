import tables
type
  ValueKind = enum
    vkInt, vkStr, vkList, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: {"id": Value(kind: vkInt, intVal: 1), "label": Value(kind: vkStr, strVal: "first"), "tags": Value(kind: vkList, listVal: newSeq[Value]())}.toTable),
    Value(kind: vkTable, tableVal: {"id": Value(kind: vkInt, intVal: 2), "label": Value(kind: vkStr, strVal: "second"), "tags": Value(kind: vkList, listVal: newSeq[Value]())}.toTable),
    Value(kind: vkTable, tableVal: {"id": Value(kind: vkInt, intVal: 3), "label": Value(kind: vkStr, strVal: "third"), "tags": Value(kind: vkList, listVal: newSeq[Value]())}.toTable)
]
