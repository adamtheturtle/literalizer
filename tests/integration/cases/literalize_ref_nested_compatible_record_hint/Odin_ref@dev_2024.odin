#+feature dynamic-literals
package main
Record1 :: struct { items: [dynamic]any }
Record0 :: struct { outer: Record1 }

main :: proc() {
record_data := Record1{
	items = [dynamic]any{
		1,
		2,
	},
}
my_data := Record0{
	outer = record_data,
}
_ = my_data
}
