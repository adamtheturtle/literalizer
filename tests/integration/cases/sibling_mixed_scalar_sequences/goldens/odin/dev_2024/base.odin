#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"left" = [dynamic]any{1, "one"},
	"right" = [dynamic]any{2, "two"},
}
_ = my_data
}
