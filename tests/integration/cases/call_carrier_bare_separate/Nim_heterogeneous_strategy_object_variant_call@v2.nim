{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
template make_widget(args: varargs[untyped]) = discard
make_widget(@[Value(kind: vkInt, intVal: 1)], @[Value(kind: vkStr, strVal: "text")])
