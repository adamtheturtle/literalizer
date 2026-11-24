#+feature dynamic-literals
package main
Record1 :: struct { k: [dynamic]any }
Record0 :: struct { h: [dynamic]any }

main :: proc() {
my_data := Record0{
	h = [dynamic]any{
		1,
		"a",
		[dynamic]any{
			2,
			"b",
		},
		Record1{
			k = [dynamic]any{
				true,
			},
		},
	},
}
_ = my_data
}
