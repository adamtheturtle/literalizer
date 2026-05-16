package main

func main() {
my_data := map[string]any{
	"project": "alpha",
	"lead_task": map[string]any{"id": 100, "description": "first task", "is_done": false, "blocks": []int{102, 103}},
}
_ = my_data
}
