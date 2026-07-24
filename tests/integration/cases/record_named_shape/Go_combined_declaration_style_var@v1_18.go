package main

func main() {
var my_data = []map[string]any{
	{"id": 100, "label": "first item", "enabled": false, "related_ids": []int{102, 103}},
	{"id": 101, "label": "second item", "enabled": true, "related_ids": []int{100}},
}
my_data = []map[string]any{
	{"id": 100, "label": "first item", "enabled": false, "related_ids": []int{102, 103}},
	{"id": 101, "label": "second item", "enabled": true, "related_ids": []int{100}},
}
_ = my_data
}
