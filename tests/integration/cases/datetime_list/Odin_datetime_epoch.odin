#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1705321800,
	1717228800,
}
_ = my_data
}
