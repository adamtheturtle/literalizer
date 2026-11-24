#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0b101010,
	3.14,
	true,
	false,
	"hello \"world\"",
}
_ = my_data
}
