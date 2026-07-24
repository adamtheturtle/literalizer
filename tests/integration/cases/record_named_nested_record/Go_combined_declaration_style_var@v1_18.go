package main

func main() {
var my_data = map[string]any{
	"project": "alpha",
	"lead_item": map[string]any{"id": 100, "label": "first item", "enabled": false, "related_ids": []int{102, 103}},
}
my_data = map[string]any{
	"project": "alpha",
	"lead_item": map[string]any{"id": 100, "label": "first item", "enabled": false, "related_ids": []int{102, 103}},
}
_ = my_data
}
