#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1, [dynamic]any{}},
	[dynamic]any{2, [dynamic]any{3}},
}
_ = my_data
}
