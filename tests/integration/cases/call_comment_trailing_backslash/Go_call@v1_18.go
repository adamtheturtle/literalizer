package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{1, 1, 1, 2}
    if eventIndex >= 4 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func process(value int) int { observeEvent(1); observeEvent(value); return value + 100 }
func verify_events() { if eventIndex != 4 { panic("missing receiver events") } }

func main() {
process(1)  // trail \ .
process(2)  // second
verify_events()
}
