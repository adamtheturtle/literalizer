val expectedEvents = listOf(1, 42, 1, 42, 1, 142)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 6 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun make_widget(count: Int): Int { observeEvent(1); observeEvent(count); return count + 100 }
fun verify_events() { check(eventIndex == 6) }
var my_data = 42
make_widget(count = my_data)
my_data = make_widget(count = my_data)
make_widget(count = my_data)
verify_events()
