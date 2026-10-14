package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(42)
my_data = make_widget(42) // note
}
