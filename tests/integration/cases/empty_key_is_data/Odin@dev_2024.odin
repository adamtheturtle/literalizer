#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"" = "external_value"},
}
_ = my_data
}
