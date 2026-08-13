#+feature dynamic-literals
package main

main :: proc() {
deep := [dynamic]any{
	[dynamic]any{
		1,
		2,
	},
	[dynamic]any{
		3,
		4,
	},
}
my_data := map[string]any{
	"a" = map[string]any{
		"b" = map[string]any{
			"c" = deep,
		},
	},
}
_ = my_data
}
