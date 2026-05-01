#+feature dynamic-literals
package main

main :: proc() {
my_var := map[string]any{
	"_" = "_",
}
item_var := map[string]any{
	"_" = "_",
}
my_data := map[string]any{
	"key" = my_var,
	"items" = [dynamic]any{item_var, map[string]any{"fallback" = "value"}},
}
_ = my_data
}
