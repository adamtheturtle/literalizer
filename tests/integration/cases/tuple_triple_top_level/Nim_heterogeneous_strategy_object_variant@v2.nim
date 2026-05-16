type
  ValueKind = enum
    vkInt, vkStr, vkBool
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkBool: boolVal: bool
var my_data = @[
    Value(kind: vkInt, intVal: 1),
    Value(kind: vkStr, strVal: "email"),
    Value(kind: vkBool, boolVal: true)
]
