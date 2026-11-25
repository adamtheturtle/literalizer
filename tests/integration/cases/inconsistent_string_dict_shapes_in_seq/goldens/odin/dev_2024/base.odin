#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"first" = "Alice", "last" = "Smith"},
	map[string]any{"first" = "Bob", "middle" = "Quincy"},
}
_ = my_data
}
