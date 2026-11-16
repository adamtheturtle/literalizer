object Fixture_call_comment_trailing_backslash_Scala_call {
private val expectedEvents = List(1, 1, 1, 2)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 4 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def process(value : Int): Int = { observeEvent(1); observeEvent(value); value + 100 }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 4) }
process(value = 1)  // trail \ .
process(value = 2)  // second
verify_events()
}
