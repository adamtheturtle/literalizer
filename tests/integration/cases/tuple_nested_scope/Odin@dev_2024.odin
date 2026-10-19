#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"x" = [dynamic]any{1, [dynamic]any{2, [dynamic]any{3}}},
}
_ = my_data
}
