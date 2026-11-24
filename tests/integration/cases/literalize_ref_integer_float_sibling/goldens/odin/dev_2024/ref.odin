#+feature dynamic-literals
package main

main :: proc() {
integer_value := 1.0
my_data := [dynamic]any{
	integer_value,
	1.5,
}
_ = my_data
}
