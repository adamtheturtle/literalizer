#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"timestamp" = "2020-01-01T00:00:00+00:00"},
	map[string]any{},
}
_ = my_data
}
