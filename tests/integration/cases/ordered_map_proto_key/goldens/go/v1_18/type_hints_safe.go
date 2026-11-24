package main

func main() {
my_data := [][2]any{
	{"__proto__", map[string]int{"x": 1}},
	{"ordinary", 2},
}
_ = my_data
}
