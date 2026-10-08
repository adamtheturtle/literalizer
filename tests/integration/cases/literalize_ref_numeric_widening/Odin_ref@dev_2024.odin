#+feature dynamic-literals
package main

main :: proc() {
floating_value := 1.5
integer_value := 2.0
my_data := [dynamic]any{
	floating_value,
	integer_value,
}
_ = my_data
}
