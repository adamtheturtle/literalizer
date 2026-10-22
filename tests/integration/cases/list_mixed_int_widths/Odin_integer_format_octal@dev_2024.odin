#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o1,
	0o20000000000000,
}
_ = my_data
}
