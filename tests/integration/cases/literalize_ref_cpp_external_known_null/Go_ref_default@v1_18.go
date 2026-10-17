package main
func consume_widget(args ...any) any { return nil }

func main() {
var item any = nil
var my_data any = nil
consume_widget(my_data)
my_data = item
consume_widget(my_data)
}
