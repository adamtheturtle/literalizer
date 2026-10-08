#+feature dynamic-literals
package main
Record0 :: struct { a: int }

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{Record0{ a = 1 }},
	[dynamic]any{Record0{ a = 2 }},
}
_ = my_data
}
