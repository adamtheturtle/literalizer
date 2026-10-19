#+feature dynamic-literals
package main
Record0 :: struct { a: [dynamic]any }

main :: proc() {
my_data := Record0{
	a = [dynamic]any{
		1,
		[dynamic]any{},
	},
}
_ = my_data
}
