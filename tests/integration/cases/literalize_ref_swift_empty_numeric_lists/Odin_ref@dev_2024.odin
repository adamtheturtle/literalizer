#+feature dynamic-literals
package main

main :: proc() {
empty_values := [dynamic]any{}
integer_values := [dynamic]any{
	1,
}
float_values := [dynamic]any{
	1.5,
}
my_data := [dynamic]any{
	empty_values,
	integer_values,
	float_values,
}
_ = my_data
}
