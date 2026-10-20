#+feature dynamic-literals
package main

main :: proc() {
my_value := [dynamic]any{
	1,
	2,
}
my_data := my_value
_ = my_data
}
