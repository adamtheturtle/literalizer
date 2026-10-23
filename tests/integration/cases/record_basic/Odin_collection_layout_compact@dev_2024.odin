#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"id" = 1,
	"label" = "She said \"hello\", then waved",
	"enabled" = false,
	"related_ids" = [dynamic]any{1, 2, 3},
}
_ = my_data
}
