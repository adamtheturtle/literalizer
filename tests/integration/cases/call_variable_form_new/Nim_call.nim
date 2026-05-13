proc make_widget[T0](count: T0): int {.discardable.} = 0
var result = %* make_widget(42)
