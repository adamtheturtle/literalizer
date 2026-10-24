#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"k" = "2040-01-01T00:00:00+00:00"},
	map[string]any{"k" = 1},
}
_ = my_data
}
