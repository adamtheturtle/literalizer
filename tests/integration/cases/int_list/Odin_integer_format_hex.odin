#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0x1,
	0x2,
	0x3,
}
_ = my_data
}
