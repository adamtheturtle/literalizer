#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0.0,
	1.0,
	1500.0,
	0.001,
	1e16,
}
_ = my_data
}
