#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"timestamp" = 1577836800},
	map[string]any{},
}
_ = my_data
}
