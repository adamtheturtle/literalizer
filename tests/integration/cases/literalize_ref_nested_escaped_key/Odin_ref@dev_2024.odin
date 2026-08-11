#+feature dynamic-literals
package main

main :: proc() {
foo := map[string]any{
	"_" = "_",
}
my_data := map[string]any{
	"mapping" = map[string]any{"value" = foo},
	"items" = [dynamic]any{map[string]any{"other" = 1}, foo},
}
_ = my_data
}
