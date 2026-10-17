#+feature dynamic-literals
package main

main :: proc() {
external_value := map[string]any{
	"_" = "_",
}
my_data := [dynamic]any{
	external_value,
}
_ = my_data
}
