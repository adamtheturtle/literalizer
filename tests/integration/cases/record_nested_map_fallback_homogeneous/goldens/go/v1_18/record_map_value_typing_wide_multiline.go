package main
type Record1 struct {
	Kind string
	PrId string
}
type Record0 struct {
	Name string
	Input Record1
	Expected map[string]any
}

func main() {
my_data := []Record0{
	Record0{
		Name: "test_1",
		Input: Record1{
			Kind: "create",
			PrId: "pr_1",
		},
		Expected: map[string]any{
			"pr_id": "pr_1",
			"status": "draft",
		},
	},
	Record0{
		Name: "test_2",
		Input: Record1{
			Kind: "publish",
			PrId: "pr_1",
		},
		Expected: map[string]any{
			"error": "invalid_operation",
		},
	},
}
_ = my_data
}
