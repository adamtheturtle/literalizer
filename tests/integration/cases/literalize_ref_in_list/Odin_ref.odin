#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	x,
	y,
}
_ = my_data
}
