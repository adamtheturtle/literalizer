#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"b" = map[string]any{"k" = 1},
	"a" = map[string]any{"k" = "2040-01-01T00:00:00+00:00"},
}
_ = my_data
}
