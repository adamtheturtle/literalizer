#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"__proto__" = map[string]any{"x" = 1},
	"ordinary" = 2,
}
_ = my_data
}
