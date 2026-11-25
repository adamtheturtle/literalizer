import json
import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 42, 1, 42, 1, 142]
    doAssert eventIndex < 6 and actual == expected[eventIndex]
    inc eventIndex
proc make_widget(count: int): JsonNode {.discardable.} =
    observeEvent(1); observeEvent(count)
    %(count + 100)
proc make_widget(count: JsonNode): JsonNode {.discardable.} =
    observeEvent(1); observeEvent(count.getInt())
    %(count.getInt() + 100)
proc verify_events() = doAssert eventIndex == 6
var my_data = %* 42
make_widget(my_data)
my_data = make_widget(my_data)
make_widget(my_data)
verify_events()
