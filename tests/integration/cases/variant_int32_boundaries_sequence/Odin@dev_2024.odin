#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-2147483648,
	-2147483647,
	[dynamic]any{0},
}
_ = my_data
}
