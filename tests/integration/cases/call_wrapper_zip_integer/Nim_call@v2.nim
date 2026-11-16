import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 1, 2, 101, 3, 42]
    doAssert eventIndex < 6 and actual == expected[eventIndex]
    inc eventIndex
proc process(value: int): int {.discardable.} =
    observeEvent(1); observeEvent(value)
    value + 100
proc process(value: JsonNode): int {.discardable.} =
    observeEvent(1); observeEvent(value.getInt())
    value.getInt() + 100
proc emit(actual: int, zipped: int) =
    observeEvent(2); observeEvent(actual)
    observeEvent(3); observeEvent(zipped)
proc verify_events() = doAssert eventIndex == 6
emit(process(1), 42)
verify_events()
