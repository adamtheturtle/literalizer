{.warning[UnusedImport]:off.}
proc make_widget[T0](value: T0): int {.discardable.} = 0
var my_data = make_widget(@[1])
