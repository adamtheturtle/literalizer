#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0.0,
	1.0,
	1.5e3,
	1.0e-3,
}
_ = my_data
}
