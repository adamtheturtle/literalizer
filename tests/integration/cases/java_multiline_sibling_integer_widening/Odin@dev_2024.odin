#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{
		1,
	},
	"b" = [dynamic]any{
		1099511627776,
	},
}
_ = my_data
}
