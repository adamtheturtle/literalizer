#+feature dynamic-literals
package main
Record0 :: struct { value: [dynamic]any }

main :: proc() {
shared := Record0{
	value = [dynamic]any{
		1,
		2,
	},
}
my_data := [dynamic]any{
	shared,
	shared,
}
_ = my_data
}
