#+feature dynamic-literals
package main
Record0 :: struct { flags: [dynamic]any, values: [dynamic]any, ints: [dynamic]any, text: [dynamic]any, nested_flags: [dynamic]any, nested_values: [dynamic]any }

main :: proc() {
my_data := Record0{
	flags = [dynamic]any{
		true,
		false,
	},
	values = [dynamic]any{
		1.5,
		-2.25,
	},
	ints = [dynamic]any{
		1,
		2,
	},
	text = [dynamic]any{
		"a",
	},
	nested_flags = [dynamic]any{
		[dynamic]any{
			true,
		},
		[dynamic]any{
			false,
		},
	},
	nested_values = [dynamic]any{
		[dynamic]any{
			1.5,
		},
		[dynamic]any{
			2.25,
		},
	},
}
_ = my_data
}
