#+feature dynamic-literals
package main

main :: proc() {
my_data := map[any]struct{}{
	true = {},
	42 = {},
	"apple" = {},
}
_ = my_data
}
