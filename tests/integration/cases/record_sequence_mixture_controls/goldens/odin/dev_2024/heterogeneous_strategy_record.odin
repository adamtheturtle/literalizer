#+feature dynamic-literals
package main
Record0 :: struct { x: int }

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{[dynamic]any{1}, Record0{ x = 1 }},
	[dynamic]any{Record0{ x = 1 }, Record0{ x = 2 }},
	[dynamic]any{[dynamic]any{}, [dynamic]any{Record0{ x = 1 }}},
	[dynamic]any{[dynamic]any{}, [dynamic]any{}},
}
_ = my_data
}
