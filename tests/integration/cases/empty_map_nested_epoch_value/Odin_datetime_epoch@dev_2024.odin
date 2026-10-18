#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"nested" = map[string]any{"times" = [dynamic]any{-2208988800}}},
	map[string]any{},
}
_ = my_data
}
