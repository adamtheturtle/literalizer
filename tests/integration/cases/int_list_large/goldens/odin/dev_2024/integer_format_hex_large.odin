#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0xf4240,
	-0x4d2,
	0xff,
	-0xa,
}
_ = my_data
}
