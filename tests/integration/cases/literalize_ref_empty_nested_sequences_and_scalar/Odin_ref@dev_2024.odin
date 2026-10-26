#+feature dynamic-literals
package main

main :: proc() {
seed := 1
my_data := [dynamic]any{
	[dynamic]any{},
	[dynamic]any{[dynamic]any{}},
	seed,
}
_ = my_data
}
