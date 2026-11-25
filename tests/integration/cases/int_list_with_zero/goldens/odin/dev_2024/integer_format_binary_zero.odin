#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b0,
	0b1,
	-0b1,
}
_ = my_data
}
