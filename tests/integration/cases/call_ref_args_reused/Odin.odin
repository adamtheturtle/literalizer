#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"$ref" = "repeated_var"}, 1},
	[dynamic]any{map[string]any{"$ref" = "single_var"}, 0},
	[dynamic]any{map[string]any{"$ref" = "repeated_var"}, 8},
}
_ = my_data
}
