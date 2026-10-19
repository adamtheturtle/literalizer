#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"alpha" = [dynamic]any{2, [dynamic]any{}},
	"beta" = [dynamic]any{5, [dynamic]any{"x"}},
}
_ = my_data
}
