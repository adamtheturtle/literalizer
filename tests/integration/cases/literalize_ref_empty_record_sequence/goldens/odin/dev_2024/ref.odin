#+feature dynamic-literals
package main
Record0 :: struct { x: int }

main :: proc() {
empty_items := [dynamic]any{}
populated_items := [dynamic]any{
	Record0{ x = 1 },
}
my_data := [dynamic]any{
	empty_items,
	populated_items,
}
_ = my_data
}
