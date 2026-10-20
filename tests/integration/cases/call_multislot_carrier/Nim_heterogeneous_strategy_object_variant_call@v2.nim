{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkBool, vkFloat, vkNull, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkBool: boolVal: bool
    of vkFloat: floatVal: float
    of vkNull: discard
    of vkList: listVal: seq[Value]
template process(args: varargs[untyped]) = discard
process(1, "hello")
process("two", false)
process(3.5, nil)
