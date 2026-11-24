#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"single_map" = [dynamic]any{map[string]any{}},
	"single_list" = [dynamic]any{[dynamic]any{1}},
	"single_deep" = [dynamic]any{[dynamic]any{[dynamic]any{2}}},
}
_ = my_data
}
