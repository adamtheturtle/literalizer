import tables
type
  ValueKind = enum
    vkTime, vkStr
  Value = object
    case kind: ValueKind
    of vkTime: timeVal: string
    of vkStr: strVal: string
var my_data = {
    "vals": @[Value(kind: vkTime, timeVal: "09:30:00"), Value(kind: vkStr, strVal: "hello")]
}.toTable
