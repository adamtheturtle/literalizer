#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"value" = 1}},
	[dynamic]any{map[string]any{"value" = 1099511627776}},
}
_ = my_data
}
