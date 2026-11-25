import json
template consume_widget(args: varargs[untyped]) = discard
var shared = %* 1
var my_data = shared
consume_widget(my_data)
