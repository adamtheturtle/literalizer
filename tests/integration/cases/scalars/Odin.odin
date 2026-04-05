#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	42,
	3.14,
	true,
	false,
	"hello \"world\"",
}
_ = my_data
}
