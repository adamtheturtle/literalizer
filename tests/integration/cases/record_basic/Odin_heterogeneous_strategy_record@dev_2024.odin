#+feature dynamic-literals
package main
Record0 :: struct { id: int, description: string, is_done: bool, blocks: [dynamic]any }

main :: proc() {
my_data := Record0{
	id = 1,
	description = "She said \"hello\", then waved",
	is_done = false,
	blocks = [dynamic]any{
		1,
		2,
		3,
	},
}
_ = my_data
}
