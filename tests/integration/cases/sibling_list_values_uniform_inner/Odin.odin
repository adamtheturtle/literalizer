#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"lint" = [dynamic]any{2, [dynamic]any{1}},
	"test" = [dynamic]any{5, [dynamic]any{7}},
}
_ = my_data
}
