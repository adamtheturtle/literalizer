proc make_widget[T0](count: T0): int {.discardable.} = 0
let my_data = %* 42
my_data = make_widget(42)
// note
