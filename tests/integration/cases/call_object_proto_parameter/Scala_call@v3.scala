object Fixture_call_object_proto_parameter_Scala_call {
private val expectedEvents = List(1, 1)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 2 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def capture(__proto__: Int): Int = { observeEvent(1); observeEvent(__proto__); __proto__ + 100 }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 2) }
capture(__proto__ = 1)
verify_events()
}
