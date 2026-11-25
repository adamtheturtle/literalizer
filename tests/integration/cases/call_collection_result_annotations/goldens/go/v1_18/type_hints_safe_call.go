package main
func make_widget(args ...any) any { return nil }

func main() {
my_data := make_widget([][]int{[]int{1, 2}, []int{3}})
_ = my_data
}
