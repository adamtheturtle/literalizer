#+feature dynamic-literals
package main

main :: proc() {
my_data := map[any]struct{}{
	// before apple
	"apple" = {},
	"banana" = {},  // banana inline
	// trailing
}
_ = my_data
}
