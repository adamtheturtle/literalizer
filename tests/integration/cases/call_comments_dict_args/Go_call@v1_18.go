package main
func process(args ...any) any { return nil }

func main() {
// Test cases
process(map[string]string{"type": "create", "pr_id": "pr_1"})  // first case
process(map[string]string{"type": "update", "pr_id": "pr_2"})  // second case
// third case
process(map[string]string{"type": "delete", "pr_id": "pr_3"})
}
