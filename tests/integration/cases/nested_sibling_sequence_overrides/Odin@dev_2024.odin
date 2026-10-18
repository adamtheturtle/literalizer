#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{[dynamic]any{1}, [dynamic]any{2}},
	"b" = [dynamic]any{[dynamic]any{"x"}, [dynamic]any{"y"}},
}
_ = my_data
}
