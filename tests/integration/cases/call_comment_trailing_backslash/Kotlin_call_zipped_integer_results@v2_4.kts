val expectedEvents = listOf(1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 12 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun process(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun emit(actual: Int, zipped: Int) { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped) }
fun verify_events() { check(eventIndex == 12) }
emit(process(value = 1), 41)
emit(process(value = 2), 42)
verify_events()
