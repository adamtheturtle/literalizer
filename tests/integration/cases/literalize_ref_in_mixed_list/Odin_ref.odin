#+feature dynamic-literals
package main

main :: proc() {
ref_x := map[string]any{
	"_" = "_",
}
my_data := [dynamic]any{
	ref_x,
	1,
	2,
}
_ = my_data
}
