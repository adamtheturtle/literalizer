#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"name" = "Alice", "age" = 30},
	map[string]any{"name" = "Bob", "age" = 25},
}
_ = my_data
}
