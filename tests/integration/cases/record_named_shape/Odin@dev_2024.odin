#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"id" = 100, "label" = "first item", "enabled" = false, "related_ids" = [dynamic]any{102, 103}},
	map[string]any{"id" = 101, "label" = "second item", "enabled" = true, "related_ids" = [dynamic]any{100}},
}
_ = my_data
}
