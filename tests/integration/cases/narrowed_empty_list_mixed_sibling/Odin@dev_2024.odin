#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{1, "two"},
	[dynamic]any{},
}
_ = my_data
}
