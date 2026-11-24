#+feature dynamic-literals
package main

main :: proc() {
one := 1
two := "s"
my_data := [dynamic]any{
	one,
	two,
}
_ = my_data
}
