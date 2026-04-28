#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{
	"apple" = {},
	"banana" = {},
	"cherry" = {}
}
_ = my_data
}
