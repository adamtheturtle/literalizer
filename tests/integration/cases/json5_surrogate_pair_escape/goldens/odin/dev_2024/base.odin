#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"astral" = "😀",
	"mixed" = "a😀b",
	"count" = 2,
	"list" = [dynamic]any{"😀", 1},
	"nested" = map[string]any{"inner" = "😀"},
}
_ = my_data
}
