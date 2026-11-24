#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"entries" = [dynamic]any{map[string]any{"id" = 1}},
}
_ = my_data
}
