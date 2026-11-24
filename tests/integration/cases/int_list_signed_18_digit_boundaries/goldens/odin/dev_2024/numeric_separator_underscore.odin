#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	999_999_999_999_999_999,
	-999_999_999_999_999_999,
}
_ = my_data
}
