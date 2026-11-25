package main

func main() {
my_data := map[string]map[string]any{
	"first": map[string]any{"items": []any{1, map[string]int{"value": 2}}},
	"second": map[string]any{"items": []any{1, map[string]int{"value": 3}}},
}
_ = my_data
}
