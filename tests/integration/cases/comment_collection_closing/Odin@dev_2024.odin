#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	// closing
}
_ = my_data
}
