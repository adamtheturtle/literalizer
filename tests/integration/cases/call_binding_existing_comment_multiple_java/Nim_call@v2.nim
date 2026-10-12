import json
proc make_widget[T0](count: T0): int {.discardable.} = 0
var my_data = %* nil
my_data = make_widget(42) // note
// extra
