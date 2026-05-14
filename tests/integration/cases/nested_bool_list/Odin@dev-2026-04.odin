#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{true, false},
	[dynamic]any{true, true},
}
_ = my_data
}
