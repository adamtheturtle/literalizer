#+feature dynamic-literals
package main
Record0 :: struct { a: int, b: string }

main :: proc() {
my_data := Record0{
	a = 1,
	b = "x",
}
_ = my_data
}
