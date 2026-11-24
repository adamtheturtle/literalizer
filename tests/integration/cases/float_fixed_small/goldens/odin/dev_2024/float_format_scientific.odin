#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1.0e-9,
	-1.0e-9,
}
_ = my_data
}
