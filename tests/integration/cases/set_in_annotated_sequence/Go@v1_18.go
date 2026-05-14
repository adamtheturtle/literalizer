package main

func main() {
my_data := []any{
	map[any]struct{}{},
	map[int]struct{}{1: struct{}{}, 2: struct{}{}},
	[]any{},
}
_ = my_data
}
