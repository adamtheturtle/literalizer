#+feature dynamic-literals
package main
Record0 :: struct { values: map[string]any, flag: bool, direct_arrays: [dynamic]any }

main :: proc() {
my_data := Record0{
	values = map[string]any{
		"wide" = [dynamic]any{
			[dynamic]any{
				2208988800,
			},
			[dynamic]any{},
		},
		"narrow" = [dynamic]any{
			[dynamic]any{
				946684800,
			},
		},
		"negative" = [dynamic]any{
			[dynamic]any{
				-2208988800,
			},
		},
		"shifted" = [dynamic]any{
			[dynamic]any{
				2208988800,
			},
		},
		"mixed_width" = [dynamic]any{
			[dynamic]any{
				946684800,
			},
			[dynamic]any{
				2208988800,
			},
		},
		"text" = "preserve",
	},
	flag = true,
	direct_arrays = [dynamic]any{
		[dynamic]any{
			2208988800,
		},
		[dynamic]any{},
	},
}
my_data = Record0{
	values = map[string]any{
		"wide" = [dynamic]any{
			[dynamic]any{
				2208988800,
			},
			[dynamic]any{},
		},
		"narrow" = [dynamic]any{
			[dynamic]any{
				946684800,
			},
		},
		"negative" = [dynamic]any{
			[dynamic]any{
				-2208988800,
			},
		},
		"shifted" = [dynamic]any{
			[dynamic]any{
				2208988800,
			},
		},
		"mixed_width" = [dynamic]any{
			[dynamic]any{
				946684800,
			},
			[dynamic]any{
				2208988800,
			},
		},
		"text" = "preserve",
	},
	flag = true,
	direct_arrays = [dynamic]any{
		[dynamic]any{
			2208988800,
		},
		[dynamic]any{},
	},
}
_ = my_data
}
