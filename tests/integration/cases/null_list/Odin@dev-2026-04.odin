#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	nil,
	nil,
}
_ = my_data
}
