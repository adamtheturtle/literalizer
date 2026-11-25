package main
func consume_widget(args ...any) any { return nil }

func main() {
missing := []int{
	1,
	2,
}
my_data := missing
consume_widget(my_data)
}
