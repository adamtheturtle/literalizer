type
  ValueKind = enum
    vkStr, vkInt
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
var my_data = @[
    Value(kind: vkStr, strVal: "hello"),
    Value(kind: vkInt, intVal: 42)
]
