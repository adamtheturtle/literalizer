#+feature dynamic-literals
package main
Record0 :: struct { scores: [dynamic]any, args: [dynamic]any }

main :: proc() {
my_data := Record0{
	scores = [dynamic]any{
		10,
		20,
		30,
	},
	args = [dynamic]any{
		1,
		"email",
		"a@gmail.com",
		100,
	},
}
_ = my_data
}
