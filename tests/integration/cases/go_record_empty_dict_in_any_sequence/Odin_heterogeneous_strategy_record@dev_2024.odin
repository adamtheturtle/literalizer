#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{},
}
_ = my_data
}
