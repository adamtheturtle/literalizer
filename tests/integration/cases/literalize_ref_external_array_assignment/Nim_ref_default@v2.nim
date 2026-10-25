template consume_widget(args: varargs[untyped]) = discard
var shared = @[
    1,
    2
]
var my_data = @[
    0
]
consume_widget(my_data)
my_data = shared
consume_widget(my_data)
