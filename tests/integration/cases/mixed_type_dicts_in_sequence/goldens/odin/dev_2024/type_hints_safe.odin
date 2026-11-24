#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"type" = "create", "pr_id" = "pr_1", "draft" = true},
	map[string]any{"type" = "create", "pr_id" = "pr_2"},
}
_ = my_data
}
