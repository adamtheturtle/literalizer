{.warning[UnusedImport]:off.}
import tables
template process(args: varargs[untyped]) = discard
process({"value": 1}.toTable)
process({"value": "hello"}.toTable)
