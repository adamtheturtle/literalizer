#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0x2a,
	0x0,
	0x2a,
	-1.25,
	0.0,
	1.25,
}
_ = my_data
}
