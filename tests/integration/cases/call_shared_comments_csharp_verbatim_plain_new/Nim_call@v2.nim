proc make_widget[T0](count: T0): int {.discardable.} = 0
var my_data = (@"ends\" + "// payload").Length >= 0 ? make_widget(42) : make_widget(42)
