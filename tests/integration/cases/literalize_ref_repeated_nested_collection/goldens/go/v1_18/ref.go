package main

func main() {
Shared := []any{
	[]int{1, 2},
	map[string]int{"value": 1},
}
my_data := []any{
	Shared,
	Shared,
}
_ = my_data
}
