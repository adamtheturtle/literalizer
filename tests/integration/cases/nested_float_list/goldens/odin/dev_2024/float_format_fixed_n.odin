#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1.500000, 2.500000},
	[dynamic]any{3.500000, 4.500000},
}
_ = my_data
}
