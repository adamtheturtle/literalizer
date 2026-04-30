#+feature dynamic-literals
package main

main :: proc() {
x := map[string]any{
	"_" = "_",
}
my_data := [dynamic]any{
	x,
	1,
	2,
}
_ = my_data
}
