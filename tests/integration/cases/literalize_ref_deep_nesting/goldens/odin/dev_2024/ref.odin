#+feature dynamic-literals
package main

main :: proc() {
deep := [dynamic]any{
	[dynamic]any{
		"one",
		"two",
	},
	[dynamic]any{
		"three",
		"four",
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
