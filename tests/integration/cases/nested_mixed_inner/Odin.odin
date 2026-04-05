#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1, "a"},
	[dynamic]any{2, "b"},
}
_ = my_data
}
