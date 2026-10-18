#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"k" = 2208988800},
	map[string]any{"k" = 1},
}
_ = my_data
}
