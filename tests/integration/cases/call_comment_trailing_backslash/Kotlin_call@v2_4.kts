val expectedEvents = listOf(1, 1, 1, 2)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 4 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun process(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun verify_events() { check(eventIndex == 4) }
process(value = 1)  // trail \ .
process(value = 2)  // second
verify_events()
