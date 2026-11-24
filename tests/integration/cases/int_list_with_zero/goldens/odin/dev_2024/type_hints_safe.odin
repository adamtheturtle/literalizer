#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0,
	1,
	-1,
}
_ = my_data
}
