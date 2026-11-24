#+feature dynamic-literals
package main
Record0 :: struct { x: int }

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{},
	Record0{ x = 1 },
}
_ = my_data
}
