#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b1,
	0b10,
	0b11,
}
_ = my_data
}
