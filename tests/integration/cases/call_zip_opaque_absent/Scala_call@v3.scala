object Fixture_call_zip_opaque_absent_Scala_call {
private val expectedEvents = List(1, 1)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 2 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def process(value: Int): Int = { observeEvent(1); observeEvent(value); value + 100 }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 2) }
process(value = 1)
verify_events()
}
