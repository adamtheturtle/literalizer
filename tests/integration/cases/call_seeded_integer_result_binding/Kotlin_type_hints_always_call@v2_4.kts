val expectedEvents = listOf(2, 42, 1, 42, 2, 142)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 6 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun make_widget(count: Int): Int { observeEvent(1); observeEvent(count); return count + 100 }
fun consume(count: Int) { observeEvent(2); observeEvent(count) }
fun verify_events() { check(eventIndex == 6) }
var my_data: Int = 42
consume(count = my_data)
my_data = make_widget(count = 42)
consume(count = my_data)
verify_events()
