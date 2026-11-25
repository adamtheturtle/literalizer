#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	0o52,
	3.14,
	true,
	false,
	"hello \"world\"",
}
_ = my_data
}
