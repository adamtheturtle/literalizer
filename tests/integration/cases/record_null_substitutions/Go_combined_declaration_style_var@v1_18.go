package main

func main() {
var my_data = []map[string]any{
	{"missing": nil, "present": 1},
	{"missing": 2, "present": 3},
}
my_data = []map[string]any{
	{"missing": nil, "present": 1},
	{"missing": 2, "present": 3},
}
_ = my_data
}
