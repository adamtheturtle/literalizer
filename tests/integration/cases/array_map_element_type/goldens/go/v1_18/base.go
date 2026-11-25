package main

func main() {
my_data := map[string][]map[string][]map[string]any{
	"d": []map[string][]map[string]any{{"a": []map[string]any{{"b": []any{1, []any{2.5, []any{"x", []bool{true}}}}}}}},
}
_ = my_data
}
