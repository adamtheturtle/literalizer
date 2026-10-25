package main
func consume_widget(args ...any) any { return nil }

func main() {
shared := []int{
	1,
	2,
}
my_data := []int{
	0,
}
consume_widget(my_data)
my_data = shared
consume_widget(my_data)
}
