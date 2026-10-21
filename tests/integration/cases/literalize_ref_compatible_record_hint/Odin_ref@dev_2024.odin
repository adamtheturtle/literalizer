#+feature dynamic-literals
package main
Record0 :: struct { items: [dynamic]any }

main :: proc() {
record_data := Record0{
	items = [dynamic]any{
		1,
		2,
	},
}
my_data := record_data
_ = my_data
}
