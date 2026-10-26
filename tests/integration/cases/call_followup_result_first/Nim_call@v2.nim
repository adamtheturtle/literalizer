proc make_widget[T0, T1](first: T0; second: T1): int {.discardable.} = 0
proc consume[T1](argument0: int; argument1: T1) = discard
var my_data = make_widget(42, 3)
consume(my_data, 3)
