#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{"x"},
	"b" = [dynamic]any{"y"},
}
_ = my_data
}
