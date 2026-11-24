#+feature dynamic-literals
package main
Record1 :: struct { id: int, label: string }
Record0 :: struct { name: string, items: [dynamic]any }

main :: proc() {
my_data := Record0{
	name = "box",
	items = [dynamic]any{
		Record1{
			id = 1,
			label = "first",
		},
		Record1{
			id = 2,
			label = "second",
		},
	},
}
_ = my_data
}
