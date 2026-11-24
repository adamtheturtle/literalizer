import json
template make_widget(args: varargs[untyped]) = discard
var value = %* 1
make_widget(value)
