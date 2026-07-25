package main

func main() {
var my_data = []map[string]any{
	{"id": 100, "label": "first entry", "enabled": false, "related_ids": []int{102, 103}},
	{"id": 101, "label": "second entry", "enabled": true, "related_ids": []int{100}},
}
my_data = []map[string]any{
	{"id": 100, "label": "first entry", "enabled": false, "related_ids": []int{102, 103}},
	{"id": 101, "label": "second entry", "enabled": true, "related_ids": []int{100}},
}
_ = my_data
}
