#+feature dynamic-literals
package main

main :: proc() {
shared := [dynamic]any{
	1,
	2,
}
my_data := shared
my_data = shared
_ = my_data
}
