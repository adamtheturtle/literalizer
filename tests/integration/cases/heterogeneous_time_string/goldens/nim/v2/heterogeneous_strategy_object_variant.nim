import tables
type
  ValueKind = enum
    vkTime, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkTime: timeVal: string
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
var my_data = {
    "vals": Value(kind: vkList, listVal: @[Value(kind: vkTime, timeVal: "09:30:00"), Value(kind: vkStr, strVal: "hello")])
}.toTable
