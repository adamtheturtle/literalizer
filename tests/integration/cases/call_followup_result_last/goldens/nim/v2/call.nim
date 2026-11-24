proc make_widget[T0, T1](first: T0; second: T1): int {.discardable.} = 0
proc consume[T0](argument0: T0; argument1: int) = discard
var my_data = make_widget(42, 3)
consume(3, my_data)
