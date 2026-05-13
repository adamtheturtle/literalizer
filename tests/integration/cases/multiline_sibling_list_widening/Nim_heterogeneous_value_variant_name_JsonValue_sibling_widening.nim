import tables
type
  JsonValueKind = enum
    vkInt, vkStr
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = {
    "omap_value": {"first": 1}.toOrderedTable,
    "sibling_lists": {"numbers": @[JsonValue(kind: vkInt, intVal: 1), JsonValue(kind: vkInt, intVal: 2)], "strings": @[JsonValue(kind: vkStr, strVal: "x"), JsonValue(kind: vkStr, strVal: "y")]}.toTable,
    "ref_marker_present": @["$keep", "z"]
}.toTable
