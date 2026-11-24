package main
func consume_widget(args ...any) any { return nil }

func main() {
shared := 1
my_data := shared
consume_widget(my_data)
}
