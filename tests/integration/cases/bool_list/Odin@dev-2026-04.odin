#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	true,
	false,
	true,
}
_ = my_data
}
