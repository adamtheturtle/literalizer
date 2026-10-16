proc make_widget[T0](count: T0): int {.discardable.} = 0
var my_data = make_widget(0)
make_widget(my_data)
my_data = make_widget(1)
make_widget(my_data)
