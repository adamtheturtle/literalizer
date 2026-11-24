#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"item" = "existing"},
	// This comment describes the next item.
	map[string]any{"item" = "next"},
}
_ = my_data
}
