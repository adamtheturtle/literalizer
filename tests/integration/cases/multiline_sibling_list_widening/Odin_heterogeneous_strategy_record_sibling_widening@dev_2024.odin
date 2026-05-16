#+feature dynamic-literals
package main
Record1 :: struct { numbers: [dynamic]any, strings: [dynamic]any }
Record0 :: struct { omap_value: map[string]any, sibling_lists: Record1, ref_marker_present: [dynamic]any }

main :: proc() {
my_data := Record0{
	omap_value = map[string]any{
		"first" = 1,
	},
	sibling_lists = Record1{
		numbers = [dynamic]any{
			1,
			2,
		},
		strings = [dynamic]any{
			"x",
			"y",
		},
	},
	ref_marker_present = [dynamic]any{
		"$keep",
		"z",
	},
}
_ = my_data
}
