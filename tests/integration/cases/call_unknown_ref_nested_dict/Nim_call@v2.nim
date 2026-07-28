import json
template process(args: varargs[untyped]) = discard
var my_list = %* []
process([[{"inner": my_list}]])
