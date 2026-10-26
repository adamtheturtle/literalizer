proc make_widget[T0](value: T0): int {.discardable.} = 0
proc consume(argument0: int) = discard
var my_data = make_widget(42)
consume(my_data)
my_data = make_widget(42)
consume(my_data)
