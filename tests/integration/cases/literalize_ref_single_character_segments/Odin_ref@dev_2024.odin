#+feature dynamic-literals
package main

main :: proc() {
a_b_c := map[string]any{
	"_" = "_",
}
my_data := a_b_c
_ = my_data
}
