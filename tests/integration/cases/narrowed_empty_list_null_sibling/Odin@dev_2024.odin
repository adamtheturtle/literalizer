#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{nil},
	[dynamic]any{},
}
_ = my_data
}
