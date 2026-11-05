#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// first dotted key
	// second dotted key
	"a" = map[string]any{"b" = 1, "c" = 2},
}
_ = my_data
}
