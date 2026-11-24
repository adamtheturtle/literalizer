#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-9223372036854775808,
	1,
}
_ = my_data
}
