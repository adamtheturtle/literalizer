#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"numbers" = [dynamic]any{1, 2},
	"nested" = map[string]any{"inner" = [dynamic]any{3}},
	"mixed" = [dynamic]any{4, "five"},
}
_ = my_data
}
