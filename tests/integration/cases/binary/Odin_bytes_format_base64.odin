#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"SGVsbG8=",
}
_ = my_data
}
