#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b1,
	0b10000000000000000000000000000000000000000,
}
_ = my_data
}
