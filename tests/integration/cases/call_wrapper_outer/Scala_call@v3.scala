object Fixture_call_wrapper_outer_Scala_call {
private val expectedEvents = List(1, 42, 2, 142)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 4 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def process(value: Int): Int = { observeEvent(1); observeEvent(value); value + 100 }
def emit(value: Int): Unit = { observeEvent(2); observeEvent(value) }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 4) }
emit(process(value = 42))
verify_events()
}
