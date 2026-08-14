#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{
		1,
		2,
		3,
	},  // inline a
	"b" = 2,  // inline b
}
_ = my_data
}
