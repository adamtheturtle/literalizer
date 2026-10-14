proc make_widget[T0](count: T0): int {.discardable.} = 0
var my_data = make_widget(42)
my_data = make_widget(my_data)
make_widget(my_data)
