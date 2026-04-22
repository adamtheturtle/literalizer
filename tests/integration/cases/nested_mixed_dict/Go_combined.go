package main

func main() {
my_data := map[string]map[string]any{
	"outer": map[string]any{"a": 1, "b": "x", "c": nil},
}
my_data = map[string]map[string]any{
	"outer": map[string]any{"a": 1, "b": "x", "c": nil},
}
_ = my_data
}
