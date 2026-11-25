#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"d" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"b" = [dynamic]any{1, [dynamic]any{2.5, [dynamic]any{"x", [dynamic]any{true}}}}}}}},
}
_ = my_data
}
