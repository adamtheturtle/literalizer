package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{2, 42, 1, 42, 2, 142}
    if eventIndex >= 6 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func make_widget(count int) int { observeEvent(1); observeEvent(count); return count + 100 }
func consume(count int) { observeEvent(2); observeEvent(count) }
func verify_events() { if eventIndex != 6 { panic("missing receiver events") } }

func main() {
my_data := 42
consume(my_data)
my_data = make_widget(42)
consume(my_data)
verify_events()
}
