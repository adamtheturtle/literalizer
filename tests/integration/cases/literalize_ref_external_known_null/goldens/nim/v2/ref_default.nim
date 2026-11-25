import json
template consume_widget(args: varargs[untyped]) = discard
var item = %* nil
var my_data = %* nil
consume_widget(my_data)
my_data = item
consume_widget(my_data)
