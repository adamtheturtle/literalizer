#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"collection" = "alpha",
	"featured_entry" = map[string]any{"id" = 100, "label" = "first entry", "enabled" = false, "related_ids" = [dynamic]any{102, 103}},
}
_ = my_data
}
