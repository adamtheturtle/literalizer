package main

func main() {
my_data := []any{
	[]any{[]any{map[string]string{"$ref": "my_var"}, 42, "static"}},
	[]any{[]any{map[string]string{"$ref": "my_other"}, 7, "label"}},
}
_ = my_data
}
