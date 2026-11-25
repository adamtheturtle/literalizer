#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	"email",
}
_ = my_data
}
