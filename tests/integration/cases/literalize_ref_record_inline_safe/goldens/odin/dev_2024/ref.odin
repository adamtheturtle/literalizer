#+feature dynamic-literals
package main
Record0 :: struct { x: int, y: any }

main :: proc() {
my_data := Record0{
	x = 1,
	y = nil,
}
_ = my_data
}
