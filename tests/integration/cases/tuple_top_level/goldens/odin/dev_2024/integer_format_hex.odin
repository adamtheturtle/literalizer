#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0x1,
	"email",
	"a@gmail.com",
	0x64,
}
_ = my_data
}
