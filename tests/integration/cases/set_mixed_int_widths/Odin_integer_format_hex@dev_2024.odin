#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{
	0x1 = {},
	0x10000000000 = {},
}
_ = my_data
}
