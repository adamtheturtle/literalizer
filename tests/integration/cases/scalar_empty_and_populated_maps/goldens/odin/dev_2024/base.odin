#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	map[string]any{},
	map[string]any{"x" = 2},
}
_ = my_data
}
