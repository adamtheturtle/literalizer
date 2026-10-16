package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(42)
make_widget(my_data)
my_data = make_widget(my_data)
// note
make_widget(my_data)
}
