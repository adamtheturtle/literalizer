#+feature dynamic-literals
package main

main :: proc() {
x := 0
y := 0
my_data := [dynamic]any{
	x,
	y,
}
_ = my_data
}
