#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0x80000000,
	-0x7fffffff,
	[dynamic]any{0x0},
}
_ = my_data
}
