#+feature dynamic-literals
package main
Record1 :: struct { kind: string, pr_id: string }
Record0 :: struct { name: string, input: Record1, expected: map[string]any }

main :: proc() {
my_data := [dynamic]any{
	Record0{ name = "test_1", input = Record1{ kind = "create", pr_id = "pr_1" }, expected = map[string]any{"pr_id" = "pr_1", "status" = "draft"} },
	Record0{ name = "test_2", input = Record1{ kind = "publish", pr_id = "pr_1" }, expected = map[string]any{"error" = "invalid_operation"} },
}
_ = my_data
}
