type
  ValueKind = enum
    vkNull
  Value = object
    case kind: ValueKind
    of vkNull: discard
var my_data = @[
    Value(kind: vkNull)
]
