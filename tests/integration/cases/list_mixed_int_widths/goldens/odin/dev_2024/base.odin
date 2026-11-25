#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	1099511627776,
}
_ = my_data
}
