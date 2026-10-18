#+feature dynamic-literals
package main

main :: proc() {
string_map := map[string]any{
	"k" = "s",
}
my_data := [dynamic]any{
	string_map,
	map[string]any{"k" = 1},
}
_ = my_data
}
