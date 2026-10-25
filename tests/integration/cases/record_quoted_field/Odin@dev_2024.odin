#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"a-b" = 1},
}
_ = my_data
}
