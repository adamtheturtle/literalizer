object Fixture_call_binding_existing_next_line_comment_seeded_Scala_type_hints_safe_call {
private val expectedEvents = List(2, 42, 1, 42, 2, 142)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 6 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def make_widget(count: Int): Int = { observeEvent(1); observeEvent(count); count + 100 }
def consume_widget(count: Int): Unit = { observeEvent(2); observeEvent(count) }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 6) }
var my_data = 42
consume_widget(count = my_data)
my_data = make_widget(count = my_data)
// note
consume_widget(count = my_data)
verify_events()
}
