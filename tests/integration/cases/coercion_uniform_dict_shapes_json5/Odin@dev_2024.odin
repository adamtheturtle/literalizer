#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"type" = "create", "name" = "a"},
	map[string]any{"type" = "update", "name" = "b"},
}
_ = my_data
}
