type
  ValueKind = enum
    vkInt, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
var my_data = @[
    Value(kind: vkInt, intVal: 1),
    Value(kind: vkList, listVal: newSeq[Value]())
]
