#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0.000000,
	0.000000,
}
_ = my_data
}
