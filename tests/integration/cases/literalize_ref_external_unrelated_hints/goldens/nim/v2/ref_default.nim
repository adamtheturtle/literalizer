template consume_widget(args: varargs[untyped]) = discard
var missing = @[
    1,
    2
]
var my_data = missing
consume_widget(my_data)
