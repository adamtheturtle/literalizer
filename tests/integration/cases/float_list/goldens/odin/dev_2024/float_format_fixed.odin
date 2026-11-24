#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1.100000,
	-2.200000,
	3.300000,
}
_ = my_data
}
