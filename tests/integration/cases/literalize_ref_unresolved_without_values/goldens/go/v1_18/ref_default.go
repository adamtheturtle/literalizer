package main
func consume_widget(args ...any) any { return nil }

func main() {
a := 0
my_data := []int{
	a,
	1,
}
consume_widget(my_data)
}
