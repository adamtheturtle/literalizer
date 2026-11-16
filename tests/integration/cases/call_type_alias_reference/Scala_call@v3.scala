object Fixture_call_type_alias_reference_Scala_call {
private val expectedEvents = List(1, 1)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 2 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def process(value: Int): Int = { observeEvent(1); observeEvent(value); value + 100 }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 2) }
val value = 1
process(value = value)
verify_events()
}
