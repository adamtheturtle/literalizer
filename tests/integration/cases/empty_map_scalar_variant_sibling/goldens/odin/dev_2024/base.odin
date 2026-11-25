#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"count" = 1, "name" = "value"},
	map[string]any{},
}
_ = my_data
}
