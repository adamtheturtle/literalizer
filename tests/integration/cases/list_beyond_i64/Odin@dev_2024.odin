#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	9223372036854775807,
	u64(9223372036854775808),
}
_ = my_data
}
