val expectedEvents = listOf(1, 42, 2, 142)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 4 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun make_widget(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun consume(value: Int) { observeEvent(2); observeEvent(value) }
fun verify_events() { check(eventIndex == 4) }
val my_data = make_widget(value = 42)
consume(value = my_data)
verify_events()
