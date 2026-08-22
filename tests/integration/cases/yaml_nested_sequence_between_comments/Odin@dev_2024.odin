#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{
		map[string]any{"item" = "existing"},
		"kept",
		// This comment trails the first pair.
	},
	[dynamic]any{map[string]any{"item" = "next"}, "also kept"},
	// This comment describes the last pair.
	[dynamic]any{map[string]any{"item" = "last"}, "kept too"},
}
_ = my_data
}
