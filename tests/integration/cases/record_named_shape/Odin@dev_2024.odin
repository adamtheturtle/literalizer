#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"id" = 100, "description" = "first task", "is_done" = false, "blocks" = [dynamic]any{102, 103}},
	map[string]any{"id" = 101, "description" = "second task", "is_done" = true, "blocks" = [dynamic]any{100}},
}
_ = my_data
}
