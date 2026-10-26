#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"first" = map[string]any{"x" = 1},
	"second" = map[string]any{"y" = 2},
}
_ = my_data
}
