#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"sibling_lists" = map[string]any{
		"numbers" = [dynamic]any{
			1,
			2,
		},
		"strings" = [dynamic]any{
			"x",
			"y",
		},
	},
	"ref_marker_present" = [dynamic]any{
		"$keep",
		"z",
	},
}
_ = my_data
}
