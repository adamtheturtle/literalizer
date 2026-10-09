#+feature dynamic-literals
package main
Record2 :: struct { x: int }
Record1 :: struct { values: map[string]any, flag: bool }
Record3 :: struct { y: string }
Record0 :: struct { first: Record1, second: Record1 }

main :: proc() {
my_data := Record0{
	first = Record1{
		values = map[string]any{
			"outer" = map[string]any{
				"inner" = Record2{
					x = 1,
				},
			},
		},
		flag = true,
	},
	second = Record1{
		values = map[string]any{
			"outer" = map[string]any{
				"inner" = Record3{
					y = "s",
				},
			},
		},
		flag = false,
	},
}
_ = my_data
}
