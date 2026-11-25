package main

func main() {
my_data := []map[string]map[string]map[string]int{
	{"outer": map[string]map[string]int{"inner": map[string]int{"x": 1}}},
	{"outer": map[string]map[string]int{"inner": map[string]int{}}},
}
_ = my_data
}
