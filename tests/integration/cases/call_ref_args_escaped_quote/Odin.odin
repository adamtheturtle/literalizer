#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{map[string]any{"$ref" = "my_str"}},
}
_ = my_data
}
