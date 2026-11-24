#+feature dynamic-literals
package main
Record0 :: struct { values: map[string]any, flag: bool, nested_values: map[string]any, list_values: map[string]any }

main :: proc() {
my_data := Record0{
	values = map[string]any{
		"first" = 2208988800,
	},
	flag = true,
	nested_values = map[string]any{
		"first" = map[string]any{
			"nested" = 2208988800,
		},
	},
	list_values = map[string]any{
		"first" = [dynamic]any{
			2208988800,
		},
	},
}
_ = my_data
}
