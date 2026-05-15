#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"section" = map[string]any{"value" = 1},
}
_ = my_data
}
