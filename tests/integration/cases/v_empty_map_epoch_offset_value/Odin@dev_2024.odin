#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"timestamp" = "2040-01-01T03:00:00+03:00"},
	map[string]any{},
}
_ = my_data
}
