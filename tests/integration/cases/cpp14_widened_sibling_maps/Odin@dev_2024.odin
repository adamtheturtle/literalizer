#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"k" = 1},
	"b" = map[string]any{"k" = "s"},
}
_ = my_data
}
