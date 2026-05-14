#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"scores" = [dynamic]any{
		10,
		20,
		30,
	},
}
_ = my_data
}
