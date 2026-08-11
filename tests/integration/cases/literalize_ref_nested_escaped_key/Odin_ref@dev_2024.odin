#+feature dynamic-literals
package main

main :: proc() {
foo := map[string]any{
	"_" = "_",
}
my_data := map[string]any{
	"items" = [dynamic]any{map[string]any{"other" = 1}, foo},
	"mapping" = map[string]any{"value" = foo},
}
_ = my_data
}
