#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1_000_000,
	-1_234,
	255,
	-10,
}
_ = my_data
}
