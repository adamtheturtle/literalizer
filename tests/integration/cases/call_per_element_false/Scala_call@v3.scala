object Fixture_call_per_element_false_Scala_call {
private val expectedEvents = List(1, 1)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 2 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def process(data: Int): Int = { observeEvent(1); observeEvent(data); data + 100 }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 2) }
process(data = 1)
verify_events()
}
