#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-2147483649,
	-2147483648,
	2147483647,
	2147483648,
}
_ = my_data
}
