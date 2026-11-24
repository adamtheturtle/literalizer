#+feature dynamic-literals
package main
Record1 :: struct { item: int }
Record2 :: struct { item: any }
Record0 :: struct { integers: [dynamic]any, nulls: [dynamic]any, nested: [dynamic]any, reversed: [dynamic]any }

main :: proc() {
my_data := Record0{
	integers = [dynamic]any{
		[dynamic]any{},
		[dynamic]any{
			Record1{
				item = 1,
			},
		},
	},
	nulls = [dynamic]any{
		[dynamic]any{},
		[dynamic]any{
			Record2{
				item = nil,
			},
		},
	},
	nested = [dynamic]any{
		[dynamic]any{
			[dynamic]any{},
			[dynamic]any{
				Record1{
					item = 2,
				},
			},
		},
		[dynamic]any{
			[dynamic]any{
				Record1{
					item = 3,
				},
			},
			[dynamic]any{},
		},
	},
	reversed = [dynamic]any{
		[dynamic]any{
			Record1{
				item = 4,
			},
		},
		[dynamic]any{},
	},
}
_ = my_data
}
