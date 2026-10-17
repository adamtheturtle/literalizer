#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"first" = 1},
	map[string]any{"repeated" = "a"},
	map[string]any{"repeated" = "b"},
}
_ = my_data
}
