#+feature dynamic-literals
package main
Record1 :: struct { x: int }
Record0 :: struct { values: map[string]any, flag: bool }

main :: proc() {
my_data := Record0{
	values = map[string]any{
		"first" = Record1{
			x = 1,
		},
		"second" = Record1{
			x = 2,
		},
	},
	flag = true,
}
_ = my_data
}
