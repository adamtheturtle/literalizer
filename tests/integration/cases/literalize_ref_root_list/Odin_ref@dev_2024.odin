#+feature dynamic-literals
package main

main :: proc() {
whole := [dynamic]any{
	1,
	2,
}
my_data := whole
_ = my_data
}
