#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"2000-01-01T01:02:03",
	1,
}
_ = my_data
}
