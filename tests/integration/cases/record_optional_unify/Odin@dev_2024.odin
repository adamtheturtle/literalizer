#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"items" = [dynamic]any{map[string]any{"id" = 1}, map[string]any{"id" = 2, "count" = 10}, map[string]any{"id" = 3, "count" = 20}},
}
_ = my_data
}
