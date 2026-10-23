#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0.0,
	1.5,
}
_ = my_data
}
