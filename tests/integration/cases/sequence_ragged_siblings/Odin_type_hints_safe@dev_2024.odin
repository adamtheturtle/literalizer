#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{"set_task", "web", "lint_web"},
	[dynamic]any{"merge_pipelines"},
}
_ = my_data
}
