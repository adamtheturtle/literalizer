#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"outer" = map[string]any{"inner" = map[string]any{"x" = 1}}},
	map[string]any{"outer" = map[string]any{"inner" = map[string]any{}}},
}
_ = my_data
}
