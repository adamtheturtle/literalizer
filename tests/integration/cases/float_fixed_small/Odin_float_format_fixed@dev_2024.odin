#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0.000000001,
	-0.000000001,
}
_ = my_data
}
