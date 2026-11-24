#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"value" = [dynamic]any{}},
	map[string]any{"value" = [dynamic]any{1}},
}
my_data = [dynamic]any{
	map[string]any{"value" = [dynamic]any{}},
	map[string]any{"value" = [dynamic]any{1}},
}
_ = my_data
}
