#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{map[string]any{"k" = 1}},
	"b" = [dynamic]any{map[string]any{"k" = 2}},
}
_ = my_data
}
