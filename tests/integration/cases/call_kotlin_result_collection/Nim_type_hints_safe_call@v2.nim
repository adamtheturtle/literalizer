proc make_widget[T0](items: T0): int {.discardable.} = 0
var my_data = make_widget([[1, 2], [3]])
