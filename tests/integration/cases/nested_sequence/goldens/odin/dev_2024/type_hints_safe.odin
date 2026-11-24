#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	true,
	"hi",
	[dynamic]any{1, 2},
	nil,
}
_ = my_data
}
