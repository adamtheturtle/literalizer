#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
// Test cases
process(map[string]any{"type" = "create", "pr_id" = "pr_1"});  // first case
process(map[string]any{"type" = "update", "pr_id" = "pr_2"});  // second case
// third case
process(map[string]any{"type" = "delete", "pr_id" = "pr_3"});
}
