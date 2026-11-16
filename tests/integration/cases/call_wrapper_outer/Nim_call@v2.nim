import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 42, 2, 142]
    doAssert eventIndex < 4 and actual == expected[eventIndex]
    inc eventIndex
proc process(value: int): int {.discardable.} =
    observeEvent(1); observeEvent(value)
    value + 100
proc process(value: JsonNode): int {.discardable.} =
    observeEvent(1); observeEvent(value.getInt())
    value.getInt() + 100
proc emit(value: int) = observeEvent(2); observeEvent(value)
proc verify_events() = doAssert eventIndex == 4
emit(process(42))
verify_events()
