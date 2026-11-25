#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{},
	map[string]any{"value" = 1},
}
_ = my_data
}
