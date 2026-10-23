#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	1_099_511_627_776,
}
_ = my_data
}
