#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{
	-1 = {},
}
_ = my_data
}
