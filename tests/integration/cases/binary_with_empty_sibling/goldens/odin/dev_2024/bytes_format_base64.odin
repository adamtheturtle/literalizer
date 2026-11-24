#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"SGVsbG8=",
	[dynamic]any{},
}
_ = my_data
}
