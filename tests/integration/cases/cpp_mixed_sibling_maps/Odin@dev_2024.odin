#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"a" = 1}, map[string]any{"a" = nil}, 42},
	[dynamic]any{map[string]any{"a" = 1}, map[string]any{"a" = "s"}, 42},
	[dynamic]any{map[string]any{"a" = 1}, map[string]any{"a" = nil}},
	[dynamic]any{map[string]any{"a" = 1}, map[string]any{"a" = "s"}},
}
_ = my_data
}
