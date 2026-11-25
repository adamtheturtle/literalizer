#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{
	0x1 = {},
	0x2 = {},
	0x3 = {},
}
_ = my_data
}
