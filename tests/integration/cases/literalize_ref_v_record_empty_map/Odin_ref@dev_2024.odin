#+feature dynamic-literals
package main
Record0 :: struct { bound: map[string]any }

main :: proc() {
empty_map := map[string]any{}
my_data := Record0{
	bound = empty_map,
}
_ = my_data
}
