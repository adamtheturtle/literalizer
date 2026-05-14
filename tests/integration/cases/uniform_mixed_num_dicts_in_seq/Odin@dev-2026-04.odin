#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"x" = 1, "y" = 2.5},
	map[string]any{"x" = 3, "y" = 4.0},
}
_ = my_data
}
