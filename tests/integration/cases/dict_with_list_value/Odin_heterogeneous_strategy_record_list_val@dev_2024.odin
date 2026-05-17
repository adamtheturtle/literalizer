#+feature dynamic-literals
package main
Record0 :: struct { name: string, scores: [dynamic]any }

main :: proc() {
my_data := Record0{
	name = "Alice",
	scores = [dynamic]any{
		10,
		20,
		30,
	},
}
_ = my_data
}
