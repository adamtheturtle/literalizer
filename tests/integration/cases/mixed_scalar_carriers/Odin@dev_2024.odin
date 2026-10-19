#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	"a",
	2.5,
}
_ = my_data
}
