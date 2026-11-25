#+feature dynamic-literals
package main

main :: proc() {
ref_x := 3
my_data := [dynamic]any{
	ref_x,
	1,
	2,
}
_ = my_data
}
