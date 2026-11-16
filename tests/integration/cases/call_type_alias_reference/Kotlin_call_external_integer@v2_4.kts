val expectedEvents = listOf(1, 1)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 2 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun process(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun verify_events() { check(eventIndex == 2) }
val value = 1
process(value = value)
verify_events()
