val expectedEvents = listOf(2, 42, 1, 42, 2, 142)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 6 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun make_widget(value: Int): Int { observeEvent(1); observeEvent(value); return value + 100 }
fun consume(value: Int) { observeEvent(2); observeEvent(value) }
fun verify_events() { check(eventIndex == 6) }
var my_data = 42
consume(value = my_data)
my_data = make_widget(value = 42)
consume(value = my_data)
verify_events()
