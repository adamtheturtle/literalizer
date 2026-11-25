#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{map[string]any{"a" = [dynamic]any{1}}}}}}}}}}}}}}},
}
_ = my_data
}
