#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"outer" = [dynamic]any{map[string]any{"_" = 1}},
}
_ = my_data
}
