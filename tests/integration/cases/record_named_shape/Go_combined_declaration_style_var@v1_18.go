package main

func main() {
var my_data = []map[string]any{
	{"id": 100, "description": "first task", "is_done": false, "blocks": []int{102, 103}},
	{"id": 101, "description": "second task", "is_done": true, "blocks": []int{100}},
}
my_data = []map[string]any{
	{"id": 100, "description": "first task", "is_done": false, "blocks": []int{102, 103}},
	{"id": 101, "description": "second task", "is_done": true, "blocks": []int{100}},
}
_ = my_data
}
