package main

func main() {
my_data := map[string]any{
	"lists": []any{[]int{1}, []string{"x"}, []any{}},
	"maps": []any{map[string]any{"x": 1}, map[string]any{"x": "s"}},
	"empties": map[string][]int{"a": []int{1}, "b": []int{}},
}
_ = my_data
}
