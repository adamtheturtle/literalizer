{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkStr, vkInt, vkBool, vkNull
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
    of vkNull: discard
template process(args: varargs[untyped]) = discard
process("hello")
process(42)
process(true)
process(nil)
