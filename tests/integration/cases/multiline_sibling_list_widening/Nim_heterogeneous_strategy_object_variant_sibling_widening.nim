import tables
type
  ValueKind = enum
    vkInt, vkStr
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = {
    "omap_value": {"first": 1}.toOrderedTable,
    "sibling_lists": {"numbers": @[Value(kind: vkInt, intVal: 1), Value(kind: vkInt, intVal: 2)], "strings": @[Value(kind: vkStr, strVal: "x"), Value(kind: vkStr, strVal: "y")]}.toTable,
    "ref_marker_present": @["$keep", "z"]
}.toTable
