package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{1, 1}
    if eventIndex >= 2 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func capture(__proto__ int) int { observeEvent(1); observeEvent(__proto__); return __proto__ + 100 }
func verify_events() { if eventIndex != 2 { panic("missing receiver events") } }

func main() {
capture(1)
verify_events()
}
