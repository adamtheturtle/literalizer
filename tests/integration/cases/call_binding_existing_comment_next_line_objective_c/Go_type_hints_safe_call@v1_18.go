package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := 42
my_data = make_widget(my_data)
// note
make_widget(my_data)
}
