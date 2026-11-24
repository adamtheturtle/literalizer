{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
template f(args: varargs[untyped]) = discard
f(@[Value(kind: vkInt, intVal: 1), Value(kind: vkStr, strVal: "x")])
