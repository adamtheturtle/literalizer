#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-42,
	0,
	42,
	-1.250000,
	0.000000,
	1.250000,
}
_ = my_data
}
