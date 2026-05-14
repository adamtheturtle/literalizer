package main

func main() {
var my_data = map[string]any{
	"name": "Alice",
	"tags": map[any]struct{}{true: struct{}{}, 42: struct{}{}, "apple": struct{}{}},
}
my_data = map[string]any{
	"name": "Alice",
	"tags": map[any]struct{}{true: struct{}{}, 42: struct{}{}, "apple": struct{}{}},
}
_ = my_data
}
