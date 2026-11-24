import json
template process(args: varargs[untyped]) = discard
var my_str = %* "a\"b"
process(my_str)
