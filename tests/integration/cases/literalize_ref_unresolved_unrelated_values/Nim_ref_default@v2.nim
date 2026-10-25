import json
template consume_widget(args: varargs[untyped]) = discard
var a = %* 0
var my_data = %* [
    a,
    1
]
consume_widget(my_data)
