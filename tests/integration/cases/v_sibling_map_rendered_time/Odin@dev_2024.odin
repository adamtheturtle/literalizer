#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"k" = "07:30:00"},
	"b" = map[string]any{"k" = "string"},
}
_ = my_data
}
