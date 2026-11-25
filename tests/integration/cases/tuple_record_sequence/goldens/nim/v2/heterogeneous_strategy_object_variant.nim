import tables
type
  ValueKind = enum
    vkStr, vkInt, vkList, vkTable
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: {"call": Value(kind: vkStr, strVal: "send"), "args": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1), Value(kind: vkStr, strVal: "email"), Value(kind: vkStr, strVal: "a@gmail.com"), Value(kind: vkInt, intVal: 100)])}.toTable),
    Value(kind: vkTable, tableVal: {"call": Value(kind: vkStr, strVal: "recv"), "args": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 2), Value(kind: vkStr, strVal: "sms"), Value(kind: vkStr, strVal: "b@example.com"), Value(kind: vkInt, intVal: 200)])}.toTable)
]
