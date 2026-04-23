#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{1},
	"b" = [dynamic]any{"x"},
}
_ = my_data
}
