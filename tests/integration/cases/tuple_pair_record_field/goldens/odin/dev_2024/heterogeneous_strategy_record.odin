#+feature dynamic-literals
package main
Record0 :: struct { call: string, args: [dynamic]any }

main :: proc() {
my_data := Record0{
	call = "send",
	args = [dynamic]any{
		1,
		"email",
	},
}
_ = my_data
}
