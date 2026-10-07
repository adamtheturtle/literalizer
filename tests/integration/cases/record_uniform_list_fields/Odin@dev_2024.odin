#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"scores" = [dynamic]any{1, 2}},
	map[string]any{"scores" = [dynamic]any{3, 4}},
}
_ = my_data
}
