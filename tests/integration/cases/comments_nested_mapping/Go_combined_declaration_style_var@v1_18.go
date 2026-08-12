package main

func main() {
var my_data = map[string]any{
	"a": map[string]int{
		// indented
		"x": 1,
	},
	"b": 2,
}
my_data = map[string]any{
	"a": map[string]int{
		// indented
		"x": 1,
	},
	"b": 2,
}
_ = my_data
}
