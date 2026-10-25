#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	map[string]any{"a" = 2},
}
_ = my_data
}
