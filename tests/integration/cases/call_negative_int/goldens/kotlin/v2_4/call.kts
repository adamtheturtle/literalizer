val expectedEvents = listOf(1, -1, 1, -2, 1, -3)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 6 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun process(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun verify_events() { check(eventIndex == 6) }
process(value = -1)
process(value = -2)
process(value = -3)
verify_events()
