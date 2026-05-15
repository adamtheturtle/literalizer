#+feature dynamic-literals
package main

main :: proc() {
shared_var := map[string]any{
	"_" = "_",
}
my_data := [dynamic]any{
	shared_var,
	shared_var,
}
_ = my_data
}
