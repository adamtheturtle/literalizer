#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"first" = map[string]any{"x" = 1, "y" = 2},
	"second" = map[string]any{"z" = 3},
}
_ = my_data
}
