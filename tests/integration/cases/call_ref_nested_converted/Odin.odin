#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{[dynamic]any{map[string]any{"$ref" = "myVar"}, 42, "static"}},
}
_ = my_data
}
