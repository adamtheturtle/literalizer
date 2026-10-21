{.warning[UnusedImport]:off.}
import json
proc make_widget[T0, T1, T2](before: T0; populated: T1; after: T2): int {.discardable.} = 0
make_widget(newJArray(), %*([1]), newJArray())
make_widget(%*(["text"]), %*([2]), newJArray())
make_widget(newJArray(), %*(["text"]), newJArray())
make_widget(%*(["text"]), %*([2]), %*([3]))
