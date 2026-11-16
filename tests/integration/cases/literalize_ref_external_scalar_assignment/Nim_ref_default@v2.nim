import json
template consume_widget(args: varargs[untyped]) = discard
var my_data = %* 0
var shared = %* 1
my_data = shared
consume_widget(my_data)
