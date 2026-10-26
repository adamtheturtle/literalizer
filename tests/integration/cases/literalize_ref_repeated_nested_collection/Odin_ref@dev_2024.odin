#+feature dynamic-literals
package main

main :: proc() {
shared := [dynamic]any{
	[dynamic]any{1, 2},
	map[string]any{"value" = 1},
}
my_data := [dynamic]any{
	shared,
	shared,
}
_ = my_data
}
