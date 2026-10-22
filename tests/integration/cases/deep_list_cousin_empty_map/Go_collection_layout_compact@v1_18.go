package main

func main() {
my_data := []map[string][]map[string]map[string]int{
	{"items": []map[string]map[string]int{{"inner": map[string]int{"x": 1}}, {"inner": map[string]int{}}}},
	{"items": []map[string]map[string]int{{"inner": map[string]int{"x": 2}}, {"inner": map[string]int{}}}},
}
_ = my_data
}
