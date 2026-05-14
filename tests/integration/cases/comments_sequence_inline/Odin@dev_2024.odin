#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"a",  // note a
	"b",  // note b
}
_ = my_data
}
