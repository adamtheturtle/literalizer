package main

func main() {
my_data := map[string]any{
	"__proto__": map[string]int{"x": 1},
	"n": map[string]int{"__proto__": 3},
	"y": 2,
}
_ = my_data
}
