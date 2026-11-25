#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"rows" = [dynamic]any{map[string]any{"x" = 1, "y" = "a"}, map[string]any{"x" = 2, "y" = "b"}},
}
_ = my_data
}
