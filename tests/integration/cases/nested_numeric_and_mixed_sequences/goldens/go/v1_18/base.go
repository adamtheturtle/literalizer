package main

func main() {
my_data := map[string]any{
	"numbers": []any{1, 2},
	"nested": map[string][]int{"inner": []int{3}},
	"mixed": []any{4, "five"},
}
_ = my_data
}
