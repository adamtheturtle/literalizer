#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	5.0e-324,
	-5.0e-324,
	2.2250738585072014e-308,
}
_ = my_data
}
