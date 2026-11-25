#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-42,
	0,
	42,
	-1.25,
	0.0,
	1.25,
}
_ = my_data
}
