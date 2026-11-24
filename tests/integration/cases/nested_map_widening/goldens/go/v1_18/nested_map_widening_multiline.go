package main

func main() {
my_data := []map[string]map[string]any{
	{
		"input": map[string]any{
			"kind": "add",
			"item_id": "item_1",
			"urgent": true,
		},
		"expected": map[string]any{
			"item_id": "item_1",
			"state": "pending",
		},
	},
	{
		"input": map[string]any{
			"kind": "remove",
			"item_id": "item_9",
		},
		"expected": map[string]any{
			"error": "not_found",
		},
	},
}
_ = my_data
}
