#+feature dynamic-literals
package main

main :: proc() {
shared := [dynamic]any{
	1,
	2,
}
my_data := [dynamic]any{
	shared,
	shared,
}
_ = my_data
}
