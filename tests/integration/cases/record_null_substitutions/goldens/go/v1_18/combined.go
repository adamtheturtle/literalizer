package main

func main() {
my_data := [][2]any{
	{"rows", []map[string]any{{"replacement": nil, "present": 1}, {"replacement": 2, "present": 3}}},
}
my_data = [][2]any{
	{"rows", []map[string]any{{"replacement": nil, "present": 1}, {"replacement": 2, "present": 3}}},
}
_ = my_data
}
