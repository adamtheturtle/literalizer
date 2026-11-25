#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{
		map[string]any{
			"values" = [dynamic]any{
				[dynamic]any{},
			},
		},
		map[string]any{},
	},
	[dynamic]any{
		map[string]any{},
		map[string]any{
			"values" = [dynamic]any{
				[dynamic]any{},
			},
		},
	},
}
_ = my_data
}
