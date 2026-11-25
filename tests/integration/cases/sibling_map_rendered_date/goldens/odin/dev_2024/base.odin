#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"k" = "2020-01-01"},
	"b" = map[string]any{"k" = "string"},
}
_ = my_data
}
