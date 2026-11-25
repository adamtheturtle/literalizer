#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"h" = [dynamic]any{1, "a", [dynamic]any{2, "b"}, map[string]any{"k" = [dynamic]any{true}}},
}
_ = my_data
}
