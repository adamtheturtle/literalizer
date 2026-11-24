{.warning[UnusedImport]:off.}
import tables
template process(args: varargs[untyped]) = discard
process("hello")
process(42)
process(true)
