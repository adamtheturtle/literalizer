#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	// # section
	"a",
}
_ = my_data
}
