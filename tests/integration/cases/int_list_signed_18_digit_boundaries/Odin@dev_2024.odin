#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	999999999999999999,
	-999999999999999999,
}
_ = my_data
}
