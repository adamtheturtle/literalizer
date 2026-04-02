package main

func main() {
var my_data = [][2]any{
	{"name", "Alice"},
	{"scores", map[string]string{"1": "first", "2": "second"}},
}
my_data = [][2]any{
	{"name", "Alice"},
	{"scores", map[string]string{"1": "first", "2": "second"}},
}
_ = my_data
}
