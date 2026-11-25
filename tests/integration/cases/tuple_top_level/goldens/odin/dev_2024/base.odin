#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	1,
	"email",
	"a@gmail.com",
	100,
}
_ = my_data
}
