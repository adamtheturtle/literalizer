import json
import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 1]
    doAssert eventIndex < 2 and actual == expected[eventIndex]
    inc eventIndex
proc process(value: int): int {.discardable.} =
    observeEvent(1); observeEvent(value)
    value + 100
proc process(value: JsonNode): int {.discardable.} =
    observeEvent(1); observeEvent(value.getInt())
    value.getInt() + 100
proc verify_events() = doAssert eventIndex == 2
var value = %* 1
process(value)
verify_events()
