#+feature dynamic-literals
package main
Record0 :: struct { input: map[string]any }

main :: proc() {
my_data := [dynamic]any{
	Record0{ input = map[string]any{"a" = 1} },
	Record0{ input = map[string]any{"b" = 2} },
}
_ = my_data
}
