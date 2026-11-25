package main

func main() {
Actual := 42
my_data := []any{
	map[string]any{"$ref": 1},
	map[string]any{"$ref": nil},
	Actual,
}
_ = my_data
}
