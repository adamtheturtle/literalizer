#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{[dynamic]any{}, [dynamic]any{}},
}
_ = my_data
}
