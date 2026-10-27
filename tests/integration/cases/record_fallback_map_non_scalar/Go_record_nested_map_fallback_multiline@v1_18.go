package main
type Record0 struct {
	Name string
	Payload map[string]any
}

func main() {
my_data := []Record0{
	Record0{
		Name: "one",
		Payload: map[string]any{
			"scalar": 1,
			"items": []int{
				2,
				3,
			},
		},
	},
	Record0{
		Name: "two",
		Payload: map[string]any{
			"other": 2,
		},
	},
}
_ = my_data
}
