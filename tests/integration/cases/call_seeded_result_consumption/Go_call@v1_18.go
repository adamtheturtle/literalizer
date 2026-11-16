package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{2, 0, 1, 1, 2, 101}
    if eventIndex >= 6 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func make_widget(count int) int { observeEvent(1); observeEvent(count); return count + 100 }
func consume_widget(count int) { observeEvent(2); observeEvent(count) }
func verify_events() { if eventIndex != 6 { panic("missing receiver events") } }

func main() {
my_data := 0
consume_widget(my_data)
my_data = make_widget(1)
consume_widget(my_data)
verify_events()
}
