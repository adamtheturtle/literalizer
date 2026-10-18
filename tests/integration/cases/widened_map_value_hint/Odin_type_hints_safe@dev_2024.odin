#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"a" = 1},
	1,
	"x",
	true,
	2.5,
	nil,
}
_ = my_data
}
