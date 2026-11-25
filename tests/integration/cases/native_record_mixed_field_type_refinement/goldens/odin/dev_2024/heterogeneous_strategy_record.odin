#+feature dynamic-literals
package main
Record2 :: struct { value: int }
Record1 :: struct { items: [dynamic]any }
Record3 :: struct { value: string }
Record0 :: struct { first: Record1, second: Record1 }

main :: proc() {
my_data := Record0{
	first = Record1{
		items = [dynamic]any{
			1,
			Record2{
				value = 2,
			},
		},
	},
	second = Record1{
		items = [dynamic]any{
			1,
			Record3{
				value = "s",
			},
		},
	},
}
_ = my_data
}
