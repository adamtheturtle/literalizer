val expectedEvents = listOf(1, 42, 2, 142)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 4 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun process(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun emit(value: Int) { observeEvent(2); observeEvent(value) }
fun verify_events() { check(eventIndex == 4) }
emit(process(value = 42))
verify_events()
