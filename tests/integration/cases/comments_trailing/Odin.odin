#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"a",
	// trailing
}
_ = my_data
}
