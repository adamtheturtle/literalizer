{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkNull, vkStr
  Value = object
    case kind: ValueKind
    of vkNull: discard
    of vkStr: strVal: string
template process(args: varargs[untyped]) = discard
process(nil)
process("hello")
