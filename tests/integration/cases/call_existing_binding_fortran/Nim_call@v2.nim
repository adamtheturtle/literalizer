proc make_widget[T0](count: T0): int {.discardable.} = 0
template consume_widget(args: varargs[untyped]) = discard
var my_data = make_widget(0)
consume_widget(my_data)
my_data = make_widget(1)
consume_widget(my_data)
