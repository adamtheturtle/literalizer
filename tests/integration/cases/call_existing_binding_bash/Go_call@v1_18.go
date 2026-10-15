package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget(0)
my_data = make_widget(1)
make_widget(my_data)
}
