proc make_widget[T0](count: T0): int {.discardable.} = 0
template consume(args: varargs[untyped]) = discard
var my_data = make_widget(42)
consume(my_data)
my_data = make_widget(42)
consume(my_data)
