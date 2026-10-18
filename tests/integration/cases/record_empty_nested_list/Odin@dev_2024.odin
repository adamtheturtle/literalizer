#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{[dynamic]any{1, 2}, [dynamic]any{3}},
	"b" = [dynamic]any{[dynamic]any{}, [dynamic]any{1}},
}
_ = my_data
}
