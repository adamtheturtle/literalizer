#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"a" = 1},
	map[string]any{},
}
_ = my_data
}
