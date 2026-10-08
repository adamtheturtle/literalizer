#+feature dynamic-literals
package main

main :: proc() {
x := [dynamic]any{
	1,
	2,
}
my_data := x
_ = my_data
}
