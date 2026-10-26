import json
type
  ValueKind = enum
    vkDateTime, vkInt
  Value = object
    case kind: ValueKind
    of vkDateTime: dateTimeVal: JsonNode
    of vkInt: intVal: int
var my_data = @[
    Value(kind: vkDateTime, dateTimeVal: %*{"year": 2000, "month": 1, "day": 1, "hour": 1, "minute": 2, "second": 3}),
    Value(kind: vkInt, intVal: 1)
]
