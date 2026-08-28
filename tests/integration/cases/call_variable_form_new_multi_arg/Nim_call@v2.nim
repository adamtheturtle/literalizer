proc record_entry[T0, T1, T2](s: T0; n: T1; b: T2): int {.discardable.} = 0
var my_data = record_entry("a", 1, true)
