#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1.1,
	-2.2,
	3.3,
}
_ = my_data
}
