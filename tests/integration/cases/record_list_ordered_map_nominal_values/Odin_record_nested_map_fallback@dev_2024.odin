#+feature dynamic-literals
package main
Record1 :: struct { x: int }
Record0 :: struct { values: [dynamic]any, flag: bool }

main :: proc() {
my_data := Record0{
	values = [dynamic]any{
		map[string]any{
			"inner" = Record1{
				x = 1,
			},
		},
		map[string]any{
			"inner" = Record1{
				x = 2,
			},
		},
	},
	flag = true,
}
_ = my_data
}
