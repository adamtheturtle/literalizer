#+feature dynamic-literals
package main
Record0 :: struct { x: int }

main :: proc() {
first := [dynamic]any{
	Record0{ x = 1 },
	Record0{ x = 2 },
}
my_data := first
_ = my_data
}
