#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]struct{}{"a" = {}, "b" = {}},
}
_ = my_data
}
