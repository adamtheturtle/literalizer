#+feature dynamic-literals
package main
Record0 :: struct { vals: [dynamic]any }

main :: proc() {
my_data := Record0{
	vals = [dynamic]any{
		"09:30:00",
		"hello",
	},
}
_ = my_data
}
