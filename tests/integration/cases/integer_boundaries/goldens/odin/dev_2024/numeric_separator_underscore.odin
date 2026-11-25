#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	-9_223_372_036_854_775_808,
	u64(9_223_372_036_854_775_808),
}
_ = my_data
}
