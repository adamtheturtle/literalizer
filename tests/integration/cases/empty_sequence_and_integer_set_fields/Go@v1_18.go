package main

func main() {
my_data := map[string]any{
	"a": []any{},
	"b": map[int]struct{}{1: struct{}{}, 2: struct{}{}},
}
_ = my_data
}
