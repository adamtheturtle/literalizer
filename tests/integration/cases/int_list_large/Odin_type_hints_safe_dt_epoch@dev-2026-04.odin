#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1000000,
	-1234,
	255,
	-10,
}
_ = my_data
}
