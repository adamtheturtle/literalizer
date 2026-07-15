package main
type Record0 struct {
	Name string
	Input map[string]any
	Expected map[string]any
}

func main() {
my_data := []any{
	Record0{
		Name: "test_1",
		Input: map[string]any{
			"type": "create",
			"pr_id": "pr_1",
			"draft": true,
		},
		Expected: map[string]any{
			"pr_id": "pr_1",
			"status": "draft",
		},
	},
	Record0{
		Name: "test_2",
		Input: map[string]any{
			"type": "publish",
			"pr_id": "pr_1",
		},
		Expected: map[string]any{
			"error": "invalid_operation",
		},
	},
}
_ = my_data
}
