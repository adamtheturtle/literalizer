package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{1, 1}
    if eventIndex >= 2 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func process(data int) int { observeEvent(1); observeEvent(data); return data + 100 }
func verify_events() { if eventIndex != 2 { panic("missing receiver events") } }

func main() {
process(1)
verify_events()
}
