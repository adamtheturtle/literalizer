#+feature dynamic-literals
package main

main :: proc() {
ref_data := [dynamic]any{
	1,
	2,
}
my_data := ref_data
_ = my_data
}
