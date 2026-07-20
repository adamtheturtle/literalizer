import tables
{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkTable: tableVal: Table[string, Value]
template process(args: varargs[untyped]) = discard
process({"value": Value(kind: vkInt, intVal: 1)}.toTable)
process({"value": Value(kind: vkStr, strVal: "hello")}.toTable)
