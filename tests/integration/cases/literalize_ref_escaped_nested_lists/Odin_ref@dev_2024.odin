#+feature dynamic-literals
package main

main :: proc() {
existing := 1
my_data := [dynamic]any{
	0,
	[dynamic]any{[dynamic]any{existing}},
}
_ = my_data
}
