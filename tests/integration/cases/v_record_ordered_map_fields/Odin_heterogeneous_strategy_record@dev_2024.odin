#+feature dynamic-literals
package main
Record0 :: struct { numbers: map[string]any, words: map[string]any, nested: map[string]any, empty: map[string]any, flag: bool, nested_maps: map[string]any, empty_nested_maps: map[string]any }

main :: proc() {
my_data := Record0{
	numbers = map[string]any{
		"first" = 1,
	},
	words = map[string]any{
		"first" = "s",
	},
	nested = map[string]any{
		"first" = [dynamic]any{
			1,
			2,
		},
	},
	empty = map[string]any{},
	flag = true,
	nested_maps = map[string]any{
		"first" = map[string]any{
			"nested" = 1,
		},
	},
	empty_nested_maps = map[string]any{
		"first" = map[string]any{},
	},
}
_ = my_data
}
