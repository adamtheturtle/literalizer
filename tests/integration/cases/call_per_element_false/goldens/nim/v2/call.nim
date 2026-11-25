import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 1]
    doAssert eventIndex < 2 and actual == expected[eventIndex]
    inc eventIndex
proc process(data: int): int {.discardable.} =
    observeEvent(1); observeEvent(data)
    data + 100
proc process(data: JsonNode): int {.discardable.} =
    observeEvent(1); observeEvent(data.getInt())
    data.getInt() + 100
proc verify_events() = doAssert eventIndex == 2
process(1)
verify_events()
