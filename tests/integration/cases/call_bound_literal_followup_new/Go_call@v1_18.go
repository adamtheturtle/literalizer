package main
func make_widget(args ...any) any { return nil }
func consume(args ...any) any { return nil }

func main() {
my_data := make_widget(42)
consume(my_data)
}
