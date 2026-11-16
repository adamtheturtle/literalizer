package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42}
    if eventIndex >= 12 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func process(value int) int { observeEvent(1); observeEvent(value); return value + 100 }
func emit(actual int, zipped int) { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped) }
func verify_events() { if eventIndex != 12 { panic("missing receiver events") } }

func main() {
emit(process(1), 41)
emit(process(2), 42)
verify_events()
}
