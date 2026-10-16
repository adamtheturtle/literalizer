#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,
	"b" = "x",
	"e" = [dynamic]any{1, 2},
	"f" = map[string]any{"g" = "h"},
}
_ = my_data
}
