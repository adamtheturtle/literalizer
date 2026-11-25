#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{
		// inner note
		"b" = 1,  // inline b
	},
	"list" = [dynamic]any{
		1,  // first
		2,  // second
	},
}
_ = my_data
}
