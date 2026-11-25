#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]struct{}{},
	map[int]struct{}{1 = {}, 2 = {}},
	[dynamic]any{},
}
_ = my_data
}
