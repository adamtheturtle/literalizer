package main

func main() {
my_data := map[string]any{
	"single_map": []any{
		map[string]any{},
	},
	"single_list": []any{
		[]int{
			1,
		},
	},
	"single_deep": []any{
		[][]int{
			[]int{
				2,
			},
		},
	},
}
_ = my_data
}
