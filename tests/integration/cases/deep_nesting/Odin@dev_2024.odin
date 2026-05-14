#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"level1" = map[string]any{"level2" = map[string]any{"level3" = map[string]any{"level4" = map[string]any{"value" = "deep", "items" = [dynamic]any{"a", "b"}}}, "sibling" = 42}, "tags" = [dynamic]any{map[string]any{"name" = "tag1", "meta" = map[string]any{"priority" = 1, "labels" = [dynamic]any{"x", "y"}}}}},
}
_ = my_data
}
