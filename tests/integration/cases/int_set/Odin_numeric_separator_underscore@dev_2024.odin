#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{
	1 = {},
	2 = {},
	3 = {},
}
_ = my_data
}
