{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkStr, vkInt, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
template process(args: varargs[untyped]) = discard
process("hello", "a")
process(42, "b")
process(true, "c")
