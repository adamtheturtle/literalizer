val expectedEvents = listOf(1, 1)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 2 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun capture(__proto__: Int): Int { observeEvent(1); observeEvent(__proto__); return __proto__ + 100 }
fun verify_events() { check(eventIndex == 2) }
capture(__proto__ = 1)
verify_events()
