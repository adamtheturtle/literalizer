#+feature dynamic-literals
package main
Record0 :: struct { x: int }

main :: proc() {
my_data := [dynamic]any{
	Record0{ x = 1 },
	[dynamic]any{},
}
_ = my_data
}
