#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	"email",
	true,
}
_ = my_data
}
