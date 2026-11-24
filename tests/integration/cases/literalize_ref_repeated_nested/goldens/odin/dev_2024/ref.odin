#+feature dynamic-literals
package main

main :: proc() {
shared := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	map[string]any{"left" = shared, "right" = shared},
}
_ = my_data
}
