package main
type Record0 struct {
	Input map[string]any
}

func main() {
my_data := []Record0{
	Record0{
		Input: map[string]any{
			"a": 1,
		},
	},
	Record0{
		Input: map[string]any{
			"b": "two",
		},
	},
}
_ = my_data
}
