import json
template consume_widget(args: varargs[untyped]) = discard
var item = %* []
var my_data = %* [
    item,
    item
]
consume_widget(my_data)
