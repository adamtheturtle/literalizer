#+feature dynamic-literals
package main
Record0 :: struct { a: int }

main :: proc() {
my_data := [dynamic]any{
	Record0{ a = 1 },
	5,
}
_ = my_data
}
