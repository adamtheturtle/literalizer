package main
func consume_widget(args ...any) any { return nil }

func main() {
my_data := 0
shared := 1
consume_widget(my_data)
my_data = shared
consume_widget(my_data)
}
