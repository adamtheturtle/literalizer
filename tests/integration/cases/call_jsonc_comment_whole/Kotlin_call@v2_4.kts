val expectedEvents = listOf(1, 42)
var eventIndex = 0
fun observeEvent(actual: Int) {
    check(eventIndex < 2 && actual == expectedEvents[eventIndex])
    eventIndex++
}
fun f(a: Int): Int { observeEvent(1); observeEvent(a); return a + 100 }
fun verify_events() { check(eventIndex == 2) }
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(a = 42)
verify_events()
