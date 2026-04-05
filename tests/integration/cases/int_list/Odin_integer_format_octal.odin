#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o1,
	0o2,
	0o3,
}
_ = my_data
}
