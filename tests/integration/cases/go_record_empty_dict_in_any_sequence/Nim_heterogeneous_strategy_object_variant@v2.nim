import tables
type
  ValueKind = enum
    vkTable
  Value = object
    case kind: ValueKind
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: initTable[string, Value]())
]
