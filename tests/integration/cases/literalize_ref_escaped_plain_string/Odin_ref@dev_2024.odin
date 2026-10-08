#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0,
	[dynamic]any{[dynamic]any{"plain"}},
}
_ = my_data
}
