val expectedEvents = listOf(1, 1)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 2 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun process(data: Int): Int { observeEvent(1); observeEvent(data); return data + 100 }
fun verify_events() { check(eventIndex == 2) }
process(data = 1)
verify_events()
