#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	// line 1
	// line 2
	"a",
}
_ = my_data
}
