template consume_widget(args: varargs[untyped]) = discard
var item = @[
    1,
    2
]
var my_data = @[
    1,
    2
]
consume_widget(my_data)
my_data = item
consume_widget(my_data)
