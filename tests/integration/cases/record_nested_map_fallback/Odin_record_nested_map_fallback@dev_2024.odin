#+feature dynamic-literals
package main
Record0 :: struct { name: string, input: map[string]any, expected: map[string]any }

main :: proc() {
my_data := [dynamic]any{
	Record0{ name = "test_1", input = map[string]any{"type" = "create", "pr_id" = "pr_1", "draft" = true}, expected = map[string]any{"pr_id" = "pr_1", "status" = "draft"} },
	Record0{ name = "test_2", input = map[string]any{"type" = "publish", "pr_id" = "pr_1"}, expected = map[string]any{"error" = "invalid_operation"} },
}
_ = my_data
}
