#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{map[string]any{"item" = [dynamic]any{1}}},
	"b" = [dynamic]any{map[string]any{"item" = [dynamic]any{2, 3}}},
}
_ = my_data
}
