#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	2.500000,
	3,
}
_ = my_data
}
