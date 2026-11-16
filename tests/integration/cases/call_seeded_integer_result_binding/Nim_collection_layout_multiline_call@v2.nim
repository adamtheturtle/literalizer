import json
import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [2, 42, 1, 42, 2, 142]
    doAssert eventIndex < 6 and actual == expected[eventIndex]
    inc eventIndex
proc make_widget(count: int): JsonNode {.discardable.} =
    observeEvent(1); observeEvent(count)
    %(count + 100)
proc make_widget(count: JsonNode): JsonNode {.discardable.} =
    observeEvent(1); observeEvent(count.getInt())
    %(count.getInt() + 100)
proc consume(count: int) = observeEvent(2); observeEvent(count)
proc consume(count: JsonNode) = observeEvent(2); observeEvent(count.getInt())
proc verify_events() = doAssert eventIndex == 6
var my_data = %* 42
consume(my_data)
my_data = make_widget(42)
consume(my_data)
verify_events()
