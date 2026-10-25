package main
func consume_widget(args ...any) any { return nil }

func main() {
ref_data := []int{
	1,
	2,
}
my_data := []int{
	0,
}
consume_widget(my_data)
my_data = ref_data
consume_widget(my_data)
}
