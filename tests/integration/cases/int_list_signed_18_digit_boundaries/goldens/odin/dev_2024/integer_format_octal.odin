#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o67405553164730777777,
	-0o67405553164730777777,
}
_ = my_data
}
