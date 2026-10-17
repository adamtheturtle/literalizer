#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	5.0e-324,
	-5.0e-324,
	1.0e-310,
}
_ = my_data
}
