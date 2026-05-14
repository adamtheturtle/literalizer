#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b11110100001001000000,
	-0b10011010010,
	0b11111111,
	-0b1010,
}
_ = my_data
}
