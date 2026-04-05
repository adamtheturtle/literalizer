#+feature dynamic-literals
package main

main :: proc() {
my_data := map[any]struct{}{
	"apple" = {},  // inline comment
	// before banana
	"banana" = {},
	// trailing
}
_ = my_data
}
