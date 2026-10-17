package main
func consume_widget(args ...any) any { return nil }

func main() {
item := []int{
	1,
	2,
}
my_data := []int{
	1,
	2,
}
consume_widget(my_data)
my_data = item
consume_widget(my_data)
}
