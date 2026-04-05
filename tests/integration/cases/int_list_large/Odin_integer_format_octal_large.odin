#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o3641100,
	-0o2322,
	0o377,
	-0o12,
}
_ = my_data
}
