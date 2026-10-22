#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"key" = "hello   world", "value" = 1},
}
_ = my_data
}
