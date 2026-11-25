import json
{.warning[UnusedImport]:off.}
proc make_widget[T0](value: T0): int {.discardable.} = 0
var items: JsonNode = newJArray()
make_widget(items)
