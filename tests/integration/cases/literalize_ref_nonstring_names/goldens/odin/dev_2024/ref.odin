#+feature dynamic-literals
package main

main :: proc() {
actual := map[string]any{
	"_" = "_",
}
my_data := [dynamic]any{
	map[string]any{"$ref" = 1},
	map[string]any{"$ref" = nil},
	actual,
}
_ = my_data
}
