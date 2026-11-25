#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"rows" = [dynamic]any{map[string]any{"replacement" = -1, "present" = 1}, map[string]any{"replacement" = 2, "present" = 3}},
}
_ = my_data
}
