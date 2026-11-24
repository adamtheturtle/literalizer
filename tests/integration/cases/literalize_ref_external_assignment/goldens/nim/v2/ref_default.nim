template consume_widget(args: varargs[untyped]) = discard
var ref_data = @[
    1,
    2
]
var my_data = @[
    0
]
consume_widget(my_data)
my_data = ref_data
consume_widget(my_data)
