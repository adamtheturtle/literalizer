#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"id" = 1,
	"description" = "She said \"hello\", then waved",
	"is_done" = false,
	"blocks" = [dynamic]any{1, 2, 3},
}
_ = my_data
}
