#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"b" = nil,
	"a" = map[string]any{"y" = [dynamic]any{1.0}, "x" = false},
}
_ = my_data
}
