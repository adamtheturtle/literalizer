#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{
	1 = {},
	1_099_511_627_776 = {},
}
_ = my_data
}
