package main
type Record0 struct {
	A int
	B string
}
func consume_widget(args ...any) any { return nil }

func main() {
consume_widget(Record0{
	A: 1,
	B: "x",
})
}
