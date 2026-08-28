#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"flow" = [dynamic]any{
		1,
		// After the first element.
		2,
	},
	// Between the key and its value.
	"gap" = 3,
	// On the block scalar header.
	"block" = "Text.\n",
	"anchored" = 4,
	"alias" = 4,
	// On the alias.
}
_ = my_data
}
