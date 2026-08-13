#+feature dynamic-literals
package main
Record0 :: struct { f: map[string]any, g: int }

main :: proc() {
my_data := Record0{
	f = map[string]any{},
	g = 1,
}
_ = my_data
}
