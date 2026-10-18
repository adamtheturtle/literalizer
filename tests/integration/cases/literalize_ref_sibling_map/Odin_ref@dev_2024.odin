#+feature dynamic-literals
package main

main :: proc() {
sibling_map := map[string]any{
	"k" = 2,
}
my_data := [dynamic]any{
	map[string]any{"k" = 1},
	sibling_map,
}
_ = my_data
}
