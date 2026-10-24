#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b1,
	"email",
	"a@gmail.com",
	0b1100100,
}
_ = my_data
}
