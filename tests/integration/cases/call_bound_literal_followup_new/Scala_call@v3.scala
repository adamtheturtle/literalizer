object Fixture_call_bound_literal_followup_new_Scala_call {
private val expectedEvents = List(1, 42, 2, 142)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 4 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def make_widget(value : Int): Int = { observeEvent(1); observeEvent(value); value + 100 }
def consume(value : Int): Unit = { observeEvent(2); observeEvent(value) }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 4) }
val my_data = make_widget(value = 42)
consume(value = my_data)
verify_events()
}
