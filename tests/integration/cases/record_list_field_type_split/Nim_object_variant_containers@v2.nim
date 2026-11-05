import tables
type
  ValueKind = enum
    vkStr, vkBool, vkList, vkTable
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
    of vkList: listVal: seq[Value]
    of vkTable: tableVal: Table[string, Value]
var my_data = {
    "left": Value(kind: vkTable, tableVal: {"entries": Value(kind: vkList, listVal: @[Value(kind: vkTable, tableVal: {"kind": Value(kind: vkStr, strVal: "add"), "urgent": Value(kind: vkBool, boolVal: true)}.toTable)])}.toTable),
    "right": Value(kind: vkTable, tableVal: {"entries": Value(kind: vkList, listVal: @[Value(kind: vkTable, tableVal: {"error": Value(kind: vkStr, strVal: "not_found")}.toTable)])}.toTable)
}.toOrderedTable
