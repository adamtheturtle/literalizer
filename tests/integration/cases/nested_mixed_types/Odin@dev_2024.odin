#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1, 2},
	[dynamic]any{"a", "b"},
}
_ = my_data
}
