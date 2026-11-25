#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"a" = [dynamic]any{1}},
	map[string]any{"a" = [dynamic]any{2}},
}
_ = my_data
}
