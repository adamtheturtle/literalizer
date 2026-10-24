#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{},
	[dynamic]any{1, "value"},
	[dynamic]any{2, "other"},
}
_ = my_data
}
