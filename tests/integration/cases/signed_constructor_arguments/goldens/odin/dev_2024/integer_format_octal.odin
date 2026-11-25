#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0o52,
	0o0,
	0o52,
	-1.25,
	0.0,
	1.25,
}
_ = my_data
}
