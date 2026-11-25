#+feature dynamic-literals
package main
Record0 :: struct { a: [dynamic]any, b: [dynamic]any }

main :: proc() {
my_data := Record0{
	a = [dynamic]any{
		[dynamic]any{
			1,
			2,
		},
		[dynamic]any{
			3,
		},
	},
	b = [dynamic]any{
		[dynamic]any{},
		[dynamic]any{
			1,
		},
	},
}
_ = my_data
}
