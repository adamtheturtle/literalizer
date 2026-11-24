{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkStr, vkInt, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
proc process[T0](value: T0): int {.discardable.} = 0
type TracerType = object
template emit(self: TracerType; args: varargs[untyped]) = discard
var tracer: TracerType
tracer.emit(process("hello"))
tracer.emit(process(42))
tracer.emit(process(true))
