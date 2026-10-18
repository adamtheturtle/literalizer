#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0b10000000000000000000000000000000,
	-0b1111111111111111111111111111111,
	[dynamic]any{0b0},
}
_ = my_data
}
