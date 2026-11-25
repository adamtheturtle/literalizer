#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-0o20000000000,
	-0o17777777777,
	[dynamic]any{0o0},
}
_ = my_data
}
