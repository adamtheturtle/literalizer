import json
import tables
type
  ValueKind = enum
    vkStr, vkInt, vkFloat, vkBool, vkNull, vkDate, vkDateTime, vkBytes
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkFloat: floatVal: float
    of vkBool: boolVal: bool
    of vkNull: discard
    of vkDate: dateVal: JsonNode
    of vkDateTime: dateTimeVal: string
    of vkBytes: bytesVal: string
var my_data = {
    "s": Value(kind: vkStr, strVal: "string"),
    "i": Value(kind: vkInt, intVal: 1),
    "f": Value(kind: vkFloat, floatVal: 1.5),
    "b": Value(kind: vkBool, boolVal: true),
    "n": Value(kind: vkNull),
    "d": Value(kind: vkDate, dateVal: %*{"year": 2024, "month": 1, "day": 15}),
    "dt": Value(kind: vkDateTime, dateTimeVal: "2024-01-15T12:00:00"),
    "by": Value(kind: vkBytes, bytesVal: "48656c6c6f")
}.toTable
