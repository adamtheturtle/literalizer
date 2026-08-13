#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0o1000000000000000000000,
	0o1000000000000000000000,
}
_ = my_data
}
