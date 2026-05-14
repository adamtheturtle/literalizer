package main

func main() {
my_data := map[string]any{
	"name": "Alice",
	"tags": map[any]struct{}{true: struct{}{}, 42: struct{}{}, "apple": struct{}{}},
}
_ = my_data
}
