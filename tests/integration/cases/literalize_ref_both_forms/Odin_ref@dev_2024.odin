#+feature dynamic-literals
package main

main :: proc() {
shared_values := [dynamic]any{
	1,
	2,
}
my_data := map[string]any{
	"a" = shared_values,
}
my_data = map[string]any{
	"a" = shared_values,
}
_ = my_data
}
