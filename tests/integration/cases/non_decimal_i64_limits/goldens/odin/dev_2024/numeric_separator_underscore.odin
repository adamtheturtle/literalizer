#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-9_223_372_036_854_775_808,
	-1,
	9_223_372_036_854_775_807,
}
_ = my_data
}
