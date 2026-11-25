#+feature dynamic-literals
package main

main :: proc() {
my_data := map[int]struct{}{
	10 = {},  // comment for ten
	2 = {},  // comment for two
}
_ = my_data
}
