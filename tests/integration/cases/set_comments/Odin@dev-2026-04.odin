#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{
	"apple" = {},  // inline comment
	// before banana
	"banana" = {},
	// trailing
}
_ = my_data
}
