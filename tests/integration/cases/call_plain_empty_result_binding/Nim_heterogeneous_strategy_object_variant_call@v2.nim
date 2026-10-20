{.warning[UnusedImport]:off.}
proc make_widget[T0](value: T0): int {.discardable.} = 0
proc make_widget(value: array[0, int]): int {.discardable.} = 0
var my_data = make_widget(newSeq[string]())
