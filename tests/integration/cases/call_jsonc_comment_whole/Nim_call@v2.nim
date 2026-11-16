import std/json
var eventIndex = 0
proc observeEvent(actual: int) =
    let expected = [1, 42]
    doAssert eventIndex < 2 and actual == expected[eventIndex]
    inc eventIndex
proc f(a: int): int {.discardable.} =
    observeEvent(1); observeEvent(a)
    a + 100
proc f(a: JsonNode): int {.discardable.} =
    observeEvent(1); observeEvent(a.getInt())
    a.getInt() + 100
proc verify_events() = doAssert eventIndex == 2
# scalar heading
# second heading line
# scalar inline
# inline continuation
# scalar trailing
f(42)
verify_events()
