type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
var my_data = @[
    Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1), Value(kind: vkStr, strVal: "a")]),
    Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 2), Value(kind: vkStr, strVal: "b")])
]
