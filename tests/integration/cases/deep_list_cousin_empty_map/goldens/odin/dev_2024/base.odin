#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"items" = [dynamic]any{map[string]any{"inner" = map[string]any{"x" = 1}}, map[string]any{"inner" = map[string]any{}}}},
	map[string]any{"items" = [dynamic]any{map[string]any{"inner" = map[string]any{"x" = 2}}, map[string]any{"inner" = map[string]any{}}}},
}
_ = my_data
}
