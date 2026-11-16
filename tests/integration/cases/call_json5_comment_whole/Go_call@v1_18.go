package main
var eventIndex = 0
func observeEvent(actual int) {
    expected := []int{1, 42}
    if eventIndex >= 2 || actual != expected[eventIndex] { panic("receiver event changed") }
    eventIndex++
}
func f(a int) int { observeEvent(1); observeEvent(a); return a + 100 }
func verify_events() { if eventIndex != 2 { panic("missing receiver events") } }

func main() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42)
verify_events()
}
