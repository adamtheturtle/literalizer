#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"m" = map[string]any{}},
	map[string]any{"m" = map[string]any{}},
}
_ = my_data
}
