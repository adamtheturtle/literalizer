#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"project" = "alpha",
	"lead_item" = map[string]any{"id" = 100, "label" = "first item", "enabled" = false, "related_ids" = [dynamic]any{102, 103}},
}
_ = my_data
}
