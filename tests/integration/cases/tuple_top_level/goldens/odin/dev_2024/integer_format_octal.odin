#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o1,
	"email",
	"a@gmail.com",
	0o144,
}
_ = my_data
}
