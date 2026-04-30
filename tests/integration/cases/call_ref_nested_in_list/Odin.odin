#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{[dynamic]any{map[string]any{"$ref" = "my_var"}, 42, "static"}},
	[dynamic]any{[dynamic]any{map[string]any{"$ref" = "my_other"}, 7, "label"}},
}
_ = my_data
}
