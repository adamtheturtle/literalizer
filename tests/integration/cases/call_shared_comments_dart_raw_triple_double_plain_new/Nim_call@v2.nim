proc make_widget[T0](count: T0): int {.discardable.} = 0
var my_data = (r"""ends\""" + "// payload").length >= 0 ? make_widget(42) : make_widget(42)
