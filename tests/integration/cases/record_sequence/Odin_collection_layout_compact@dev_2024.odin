#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"id" = 1, "label" = "first", "tags" = [dynamic]any{}},
	map[string]any{"id" = 2, "label" = "second", "tags" = [dynamic]any{}},
	map[string]any{"id" = 3, "label" = "third", "tags" = [dynamic]any{}},
}
_ = my_data
}
