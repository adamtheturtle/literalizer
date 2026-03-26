package main

func main() {
my_data := []any{
    map[string]any{"type": "create", "pr_id": "pr_1", "draft": true},
    map[string]string{"type": "create", "pr_id": "pr_2"},
}
my_data = []any{
    map[string]any{"type": "create", "pr_id": "pr_1", "draft": true},
    map[string]string{"type": "create", "pr_id": "pr_2"},
}
_ = my_data
}
