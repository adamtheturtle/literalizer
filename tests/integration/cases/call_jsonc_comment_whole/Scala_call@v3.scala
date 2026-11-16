object Fixture_call_jsonc_comment_whole_Scala_call {
private val expectedEvents = List(1, 42)
private var eventIndex = 0
def observeEvent(actual: Int): Unit = {
    assert(eventIndex < 2 && actual == expectedEvents(eventIndex))
    eventIndex += 1
}
def f(a: Int): Int = { observeEvent(1); observeEvent(a); a + 100 }
def main(args: Array[String]): Unit = ()
def verify_events(): Unit = { assert(eventIndex == 2) }
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(a = 42)
verify_events()
}
