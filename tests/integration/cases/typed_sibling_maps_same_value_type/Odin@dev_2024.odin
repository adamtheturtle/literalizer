#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"s" = 1},
	map[string]any{"t" = 3},
}
_ = my_data
}
