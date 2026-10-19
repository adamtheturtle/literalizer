#+feature dynamic-literals
package main
Record0 :: struct { x: int, y: any }

main :: proc() {
value := Record0{
	x = 1,
	y = nil,
}
my_data := value
_ = my_data
}
