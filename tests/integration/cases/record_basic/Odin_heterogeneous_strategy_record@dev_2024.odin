#+feature dynamic-literals
package main
Record0 :: struct { id: int, label: string, enabled: bool, related_ids: [dynamic]any }

main :: proc() {
my_data := Record0{
	id = 1,
	label = "She said \"hello\", then waved",
	enabled = false,
	related_ids = [dynamic]any{
		1,
		2,
		3,
	},
}
_ = my_data
}
