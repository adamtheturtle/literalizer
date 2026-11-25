type
  ValueKind = enum
    vkInt, vkStr
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = @[
    Value(kind: vkInt, intVal: 1),
    Value(kind: vkStr, strVal: "email"),
    Value(kind: vkStr, strVal: "a@gmail.com"),
    Value(kind: vkInt, intVal: 100)
]
