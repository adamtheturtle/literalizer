#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"__proto__" = map[string]any{"x" = 1},
	"n" = map[string]any{"__proto__" = 3},
	"y" = 2,
}
_ = my_data
}
