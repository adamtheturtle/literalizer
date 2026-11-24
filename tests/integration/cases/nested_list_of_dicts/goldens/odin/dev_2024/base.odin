#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"name" = "Alice"}, map[string]any{"name" = "Bob"}},
	[dynamic]any{map[string]any{"name" = "Charlie"}, map[string]any{"name" = "Dave"}},
}
_ = my_data
}
