package main

func main() {
my_data := []any{
	[]any{map[string]string{"$ref": "repeated_var"}, 1},
	[]any{map[string]string{"$ref": "single_var"}, 0},
	[]any{map[string]string{"$ref": "repeated_var"}, 8},
}
my_data = []any{
	[]any{map[string]string{"$ref": "repeated_var"}, 1},
	[]any{map[string]string{"$ref": "single_var"}, 0},
	[]any{map[string]string{"$ref": "repeated_var"}, 8},
}
_ = my_data
}
