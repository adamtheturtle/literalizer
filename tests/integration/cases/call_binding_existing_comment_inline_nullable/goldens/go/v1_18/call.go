package main
func make_widget(args ...any) any { return nil }
func consume(args ...any) any { return nil }

func main() {
var my_data any = make_widget(nil)
consume(my_data)
my_data = make_widget(42) // note
consume(my_data)
}
