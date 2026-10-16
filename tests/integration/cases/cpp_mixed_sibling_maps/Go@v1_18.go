package main

func main() {
my_data := []any{
	[]any{map[string]any{"a": 1}, map[string]any{"a": nil}, 42},
	[]any{map[string]any{"a": 1}, map[string]any{"a": "s"}, 42},
	[]map[string]any{{"a": 1}, {"a": nil}},
	[]map[string]any{{"a": 1}, {"a": "s"}},
}
_ = my_data
}
