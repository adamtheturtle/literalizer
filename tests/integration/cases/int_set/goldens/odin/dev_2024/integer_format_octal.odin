#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{
	0o1 = {},
	0o2 = {},
	0o3 = {},
}
_ = my_data
}
