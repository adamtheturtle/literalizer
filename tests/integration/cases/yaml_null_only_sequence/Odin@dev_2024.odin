#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	nil,
}
_ = my_data
}
