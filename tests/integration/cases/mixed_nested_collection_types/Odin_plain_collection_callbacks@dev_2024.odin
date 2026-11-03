#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"lists" = [dynamic]any{[dynamic]any{1}, [dynamic]any{"x"}, [dynamic]any{}},
	"maps" = [dynamic]any{map[string]any{"x" = 1}, map[string]any{"x" = "s"}},
	"empties" = map[string]any{"a" = [dynamic]any{1}, "b" = [dynamic]any{}},
}
_ = my_data
}
