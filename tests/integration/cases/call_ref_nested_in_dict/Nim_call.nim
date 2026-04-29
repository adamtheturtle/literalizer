import json
template process(args: varargs[untyped]) = discard
var my_var = %* 42
process({"key": my_var, "count": 42})
