#+feature dynamic-literals
package main
Record0 :: struct { a: int, b: int, c: string }

main :: proc() {
my_data := Record0{
	a = 1,
	b = 3000000000,
	c = "x",
}
_ = my_data
}
