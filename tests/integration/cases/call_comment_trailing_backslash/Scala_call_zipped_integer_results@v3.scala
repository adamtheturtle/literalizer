object Fixture_call_comment_trailing_backslash_Scala_call_zipped_integer_results {
private val expectedEvents = List(1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 12 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def process(value: Int): Int = { observeEvent(1); observeEvent(value); value + 100 }
def emit(actual: Int, zipped: Int): Unit = { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped) }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 12) }
emit(process(value = 1), 41)
emit(process(value = 2), 42)
verify_events()
}
