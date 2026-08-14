package main

func main() {
Deep := [][]int{
	[]int{
		1,
		2,
	},
	[]int{
		3,
		4,
	},
}
my_data := map[string]map[string]map[string][][]int{
	"a": map[string]map[string][][]int{
		"b": map[string][][]int{
			"c": Deep,
		},
	},
}
_ = my_data
}
