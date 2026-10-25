#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1},
	[dynamic]any{2.5},
}
_ = my_data
}
