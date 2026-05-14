#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{[dynamic]any{1, 2}, [dynamic]any{3, 4}},
	[dynamic]any{[dynamic]any{5}},
}
_ = my_data
}
