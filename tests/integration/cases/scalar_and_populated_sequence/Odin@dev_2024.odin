#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	[dynamic]any{2, 3},
}
_ = my_data
}
