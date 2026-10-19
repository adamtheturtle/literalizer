package main

func main() {
my_data := map[string]any{
	"a": []any{map[string]int{}, map[string]int{"x": 1}},
	"b": []any{[]int{}, []int{1}},
}
_ = my_data
}
