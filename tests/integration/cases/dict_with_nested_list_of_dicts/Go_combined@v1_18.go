package main

func main() {
my_data := map[string][][]map[string]int{
	"a": [][]map[string]int{[]map[string]int{{"b": 1}}},
}
my_data = map[string][][]map[string]int{
	"a": [][]map[string]int{[]map[string]int{{"b": 1}}},
}
_ = my_data
}
