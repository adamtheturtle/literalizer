import json
template process(args: varargs[untyped]) = discard
var my_list = %* {
    "unused": "value"
}
process([[{"inner": my_list}]])
