#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	[dynamic]any{},
}
_ = my_data
}
