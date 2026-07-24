#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"id" = 100, "label" = "first entry", "enabled" = false, "related_ids" = [dynamic]any{102, 103}},
	map[string]any{"id" = 101, "label" = "second entry", "enabled" = true, "related_ids" = [dynamic]any{100}},
}
_ = my_data
}
