package main

func main() {
var my_data = [][]map[string]any{
	[]map[string]any{{"key": map[string]string{"$ref": "my_var"}, "count": 42}},
}
my_data = [][]map[string]any{
	[]map[string]any{{"key": map[string]string{"$ref": "my_var"}, "count": 42}},
}
_ = my_data
}
