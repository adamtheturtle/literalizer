#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1.5, 2.5},
	[dynamic]any{3.5, 4.5},
}
_ = my_data
}
