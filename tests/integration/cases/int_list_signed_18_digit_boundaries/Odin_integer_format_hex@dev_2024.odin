#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0xde0b6b3a763ffff,
	-0xde0b6b3a763ffff,
}
_ = my_data
}
