#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{},
	[dynamic]any{1},
	[dynamic]any{1, 2},
	[dynamic]any{1, "x", true, nil},
	[dynamic]any{1, 2, 3, 4, 5, 6, 7, 8},
}
_ = my_data
}
