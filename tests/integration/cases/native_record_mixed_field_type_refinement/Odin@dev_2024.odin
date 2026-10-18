#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"first" = map[string]any{"items" = [dynamic]any{1, map[string]any{"value" = 2}}},
	"second" = map[string]any{"items" = [dynamic]any{1, map[string]any{"value" = "s"}}},
}
_ = my_data
}
