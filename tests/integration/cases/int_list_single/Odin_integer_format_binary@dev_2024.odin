#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b1,
}
_ = my_data
}
