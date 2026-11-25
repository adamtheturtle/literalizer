{.warning[UnusedImport]:off.}
import json
template process(args: varargs[untyped]) = discard
process(%*("hello"))
process(%*(42))
process(%*(true))
