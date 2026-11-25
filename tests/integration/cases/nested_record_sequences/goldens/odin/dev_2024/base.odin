#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"a" = 1}},
	[dynamic]any{map[string]any{"a" = 2}},
}
_ = my_data
}
