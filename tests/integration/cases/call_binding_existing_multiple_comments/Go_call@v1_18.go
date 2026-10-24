package main
func make_widget(args ...any) any { return nil }
func consume_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(42)
consume_widget(my_data)
my_data = make_widget(42) // note
// extra
consume_widget(my_data)
}
