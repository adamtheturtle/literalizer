proc make_widget[T0](count: T0): int {.discardable.} = 0
proc consume_widget(argument0: int) = discard
var my_data = make_widget(0)
consume_widget(my_data)
my_data = make_widget(1)
consume_widget(my_data)
