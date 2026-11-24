import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, -1, 1, -2, 1, -3]
    doAssert eventIndex < 6 and actual == expected[eventIndex]
    inc eventIndex
proc process(value: int): int {.discardable.} =
    observeEvent(1); observeEvent(value)
    value + 100
proc process(value: JsonNode): int {.discardable.} =
    observeEvent(1); observeEvent(value.getInt())
    value.getInt() + 100
proc verify_events() = doAssert eventIndex == 6
process(-1)
process(-2)
process(-3)
verify_events()
