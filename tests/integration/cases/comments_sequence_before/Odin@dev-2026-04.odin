#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	// first
	"a",
	// second
	"b",
}
_ = my_data
}
