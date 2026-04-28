import json
import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkFloat, vkBool, vkNull, vkDate, vkDateTime, vkBytes
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkFloat: floatVal: float
    of vkBool: boolVal: bool
    of vkNull: discard
    of vkDate: dateVal: JsonNode
    of vkDateTime: dateTimeVal: JsonNode
    of vkBytes: bytesVal: string
var my_data = {
    "s": JsonValue(kind: vkStr, strVal: "string"),
    "i": JsonValue(kind: vkInt, intVal: 1),
    "f": JsonValue(kind: vkFloat, floatVal: 1.5),
    "b": JsonValue(kind: vkBool, boolVal: true),
    "n": JsonValue(kind: vkNull),
    "d": JsonValue(kind: vkDate, dateVal: %*{"year": 2024, "month": 1, "day": 15}),
    "dt": JsonValue(kind: vkDateTime, dateTimeVal: %*{"year": 2024, "month": 1, "day": 15, "hour": 12, "minute": 0, "second": 0}),
    "by": JsonValue(kind: vkBytes, bytesVal: "48656c6c6f")
}.toTable
