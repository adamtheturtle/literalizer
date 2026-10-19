#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"first" = [dynamic]any{[dynamic]any{1, "value"}, [dynamic]any{}},
	"second" = [dynamic]any{[dynamic]any{}, [dynamic]any{2, "other"}},
}
_ = my_data
}
