#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{
	// before apple
	"apple" = {},
	"banana" = {},  // banana inline
	// trailing
}
_ = my_data
}
