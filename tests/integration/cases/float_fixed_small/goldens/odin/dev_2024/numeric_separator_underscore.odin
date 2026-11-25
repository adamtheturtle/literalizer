#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1.0e-09,
	-1.0e-09,
}
_ = my_data
}
