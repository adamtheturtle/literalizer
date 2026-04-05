#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o0,
	0o1,
	-0o1,
}
_ = my_data
}
