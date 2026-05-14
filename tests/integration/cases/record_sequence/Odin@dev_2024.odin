#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"id" = 1, "label" = "first"},
	map[string]any{"id" = 2, "label" = "second"},
	map[string]any{"id" = 3, "label" = "third"},
}
_ = my_data
}
