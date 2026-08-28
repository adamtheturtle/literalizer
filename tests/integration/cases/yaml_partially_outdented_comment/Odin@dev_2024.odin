#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{
		"b" = [dynamic]any{1},
		// Outdented from the sequence, so the inner mapping claims this.
		"c" = 2,
	},
	// Outdented from the inner mapping too, so the root claims this.
	"d" = 3,
}
_ = my_data
}
