package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{1, 42, 2, 142}
    if eventIndex >= 4 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func make_widget(value int) int { observeEvent(1); observeEvent(value); return value + 100 }
func consume(value int) { observeEvent(2); observeEvent(value) }
func verify_events() { if eventIndex != 4 { panic("missing receiver events") } }

func main() {
my_data := make_widget(42)
consume(my_data)
verify_events()
}
