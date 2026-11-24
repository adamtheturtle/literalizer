#+feature dynamic-literals
package main

main :: proc() {
item_var := map[string]any{
	"_" = "_",
}
my_data := map[string]any{
	"items" = [dynamic]any{item_var, map[string]any{"fallback" = "value"}},
}
_ = my_data
}
