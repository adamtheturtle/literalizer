#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"x" = 1},
	"b" = 2,
}
_ = my_data
}
