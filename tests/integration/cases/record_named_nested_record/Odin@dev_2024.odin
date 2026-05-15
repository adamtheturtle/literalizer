#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"project" = "alpha",
	"lead_task" = map[string]any{"id" = 100, "description" = "first task", "is_done" = false, "blocks" = [dynamic]any{102, 103}},
}
_ = my_data
}
