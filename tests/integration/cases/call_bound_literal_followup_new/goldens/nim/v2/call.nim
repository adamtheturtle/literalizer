import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 42, 2, 142]
    doAssert eventIndex < 4 and actual == expected[eventIndex]
    inc eventIndex
proc make_widget(value: int): JsonNode {.discardable.} =
    observeEvent(1); observeEvent(value)
    %(value + 100)
proc make_widget(value: JsonNode): JsonNode {.discardable.} =
    observeEvent(1); observeEvent(value.getInt())
    %(value.getInt() + 100)
proc consume(value: int) = observeEvent(2); observeEvent(value)
proc consume(value: JsonNode) = observeEvent(2); observeEvent(value.getInt())
proc verify_events() = doAssert eventIndex == 4
var my_data = make_widget(42)
consume(my_data)
verify_events()
