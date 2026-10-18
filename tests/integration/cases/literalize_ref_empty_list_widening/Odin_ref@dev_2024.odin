#+feature dynamic-literals
package main

main :: proc() {
empty_values := [dynamic]any{}
integer_values := [dynamic]any{
	1,
}
my_data := [dynamic]any{
	empty_values,
	integer_values,
}
_ = my_data
}
