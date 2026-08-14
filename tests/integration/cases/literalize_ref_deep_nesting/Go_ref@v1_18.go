package main

func main() {
Deep := [][]string{
	[]string{
		"one",
		"two",
	},
	[]string{
		"three",
		"four",
	},
}
my_data := map[string]map[string]map[string][][]string{
	"a": map[string]map[string][][]string{
		"b": map[string][][]string{
			"c": Deep,
		},
	},
}
_ = my_data
}
