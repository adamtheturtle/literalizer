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
my_data := map[string]map[string]map[string]map[string]string{
	"a": map[string]map[string]map[string]string{
		"b": map[string]map[string]string{
			"c": Deep,
		},
	},
}
_ = my_data
}
