#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0x0,
	0x1,
	-0x1,
}
_ = my_data
}
