#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"key" = map[string]any{"$ref" = "my_var"}, "count" = 42}},
}
_ = my_data
}
